const handleSave = async ({ mode, action, data, callback }) => {
  try {
    // 获取所有画布数据
    const canvasList = templateData.value?.canvases
    
    if (!canvasList) {
      throw new Error('画布数据为空')
    }

    // 检查模板是否可编辑
    const checkTemplateEditable = (templateData) => {
      const currentUserId = accountStore.userInfo?.id
      const isAdmin = accountStore.userInfo?.is_staff

      // 管理员可以编辑任何模板
      if (isAdmin) {
        return true
      }

      // 非管理员只能编辑自己创建的模板
      if (templateData.creator !== currentUserId) {
        ElMessage.error('您没有权限编辑此模板')
        return false
      }

      // 已发布的模板不能编辑
      if (templateData.status === 1) { // 1 表示已发布状态
        ElMessage.error('已发布的模板不能修改')
        return false
      }

      return true
    }

    // 如果是更新操作，先检查权限
    if (currentTemplateId.value) {
      const templateData = await templateApi.getDetail(currentTemplateId.value)
      if (!checkTemplateEditable(templateData.data)) {
        if (callback) callback(false)
        return
      }
    }

    // 如果是修改已发布的模板,提示用户
    if (currentTemplateId.value) {
      const currentTemplate = await templateApi.getDetail(currentTemplateId.value)
      if (currentTemplate.data.status === 1) { // 1表示已发布状态
        const confirmResult = await ElMessageBox.confirm(
          '修改已发布的模板将重新进入审核状态,是否继续?',
          '提示',
          {
            confirmButtonText: '继续',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        if (!confirmResult) {
          if (callback) callback(false)
          return
        }
        // 设置状态为待审核
        data.status = 2
      }
    }

    // 构造要保存的数据
    const saveData = {
      ...data, // 保留原有的基本信息
      status: action === 'draft' ? 0 : 2, // 0: 草稿, 2: 待审核
      pages: canvasList.map((canvas, index) => {
        const pageData = {
          page_index: index,
          page_data: {
            elements: canvas.elements || [],
            config: {
              width: canvas.config?.width || 794,
              height: canvas.config?.height || 1123,
              backgroundColor: canvas.config?.backgroundColor || '#ffffff',
              showGrid: canvas.config?.showGrid || false,
              showGuideLine: canvas.config?.showGuideLine || true
            }
          }
        }
        return pageData
      })
    }

    // 确保数据是普通对象而不是响应式对象
    const normalizedData = JSON.parse(JSON.stringify(saveData))

    let res
    if (currentTemplateId.value) {
      res = await templateApi.update(currentTemplateId.value, normalizedData)
    } else {
      res = await templateApi.create(normalizedData)
    }
      
    if (res.status === 201 || res.status === 200) {
      // 更新本地状态
      const savedTemplate = res.data
      
      // 更新当前模板ID（如果是新创建的模板）
      if (!currentTemplateId.value && savedTemplate.id) {
        currentTemplateId.value = savedTemplate.id
        // 更新路由以反映新的模板ID
        router.replace({
          name: 'template-edit',
          params: { id: savedTemplate.id }
        })
      }
      
      // 更新默认模板数据
      defaultTemplateData.value = {
        name: savedTemplate.name,
        description: savedTemplate.description,
        category: savedTemplate.category,
        keywords: Array.isArray(savedTemplate.keywords) ? savedTemplate.keywords.join(',') : '',
        is_public: savedTemplate.is_public,
        status: savedTemplate.status
      }

      // 刷新模板列表
      if (sidebarRef.value) {
        await sidebarRef.value.loadTemplates()
      }

      // 调用成功回调
      if (callback) {
        callback(true)
      }

      ElMessage.success(action === 'draft' ? '保存草稿成功' : '提交审核成功')
    } else {
      throw new Error(res.data?.message || res.data?.detail || '保存失败')
    }
  } catch (error) {
    // 处理验证错误
    if (error.response?.status === 400) {
      const errorData = error.response.data
      if (errorData.name && Array.isArray(errorData.name)) {
        ElMessage.error(`保存失败: ${errorData.name[0]}`)
      } else if (typeof errorData === 'object') {
        const firstError = Object.values(errorData)[0]
        if (Array.isArray(firstError)) {
          ElMessage.error(`保存失败: ${firstError[0]}`)
        } else {
          ElMessage.error(`保存失败: ${JSON.stringify(errorData)}`)
        }
      } else {
        ElMessage.error('保存失败: 请检查输入数据')
      }
    } else {
      const errorMessage = error.response?.data?.message || 
                          error.response?.data?.detail || 
                          error.message || 
                          '保存失败'
      ElMessage.error(`保存失败: ${errorMessage}`)
    }

    // 调用失败回调
    if (callback) {
      callback(false)
    }
  }
}

// 处理加载完成
const handleLoadComplete = (event) => {
  if (!event.success) {
    ElMessage.error(event.error || '加载失败')
    router.push('/resume/templates')
    return
  }

  if (route.name === 'template-editor-edit') {
    handleEditTemplate(event.templateData)
  } else {
    handleUseTemplate(event.templateData, event.profileData)
  }
  
  isLoading.value = false
}

const handleEditTemplate = (templateData) => {
  if (!templateData) return
  
  defaultTemplateData.value = {
    id: templateData.id,
    name: templateData.name,
    category: templateData.category,
    description: templateData.description,
    is_public: templateData.is_public,
    keywords: templateData.keywords?.join(',') || ''
  }
  
  // 构建画布数据
  const canvasData = templateData.pages.map(page => ({
    id: page.id,
    elements: page.page_data?.elements || [],
    config: {
      ...defaultCanvasConfig,
      ...page.page_data?.config
    }
  }))
  
  if (!canvasData.length) {
    canvasData.push({
      id: generateId(),
      elements: [],
      config: defaultCanvasConfig
    })
  }
  
  updateCanvasData(canvasData)
}

const handleUseTemplate = (templateData, profileData) => {
  if (!templateData) return
  
  // 构建画布数据
  const canvasData = templateData.pages.map(page => {
    const elements = page.page_data?.elements || []
    return {
      id: page.id,
      elements: elements.map(element => {
        if (element.type === 'resume-field') {
          return mapProfileDataToElement(element, profileData)
        }
        return element
      }),
      config: {
        ...defaultCanvasConfig,
        ...page.page_data?.config
      }
    }
  })
  
  if (!canvasData.length) {
    canvasData.push({
      id: generateId(),
      elements: [],
      config: defaultCanvasConfig
    })
  }
  
  updateCanvasData(canvasData)
} 