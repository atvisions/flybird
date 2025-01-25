const handleSave = async ({ mode, action, data, callback }) => {
  try {
    console.log('准备提交的模板数据:', data)
    
    // 获取所有画布数据
    const canvasList = templateData.value?.canvases
    console.log('画布数据:', canvasList)
    
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
        console.log('处理画布', index, ':', canvas)
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
        console.log('页面', index, '数据:', pageData)
        return pageData
      })
    }

    // 确保数据是普通对象而不是响应式对象
    const normalizedData = JSON.parse(JSON.stringify(saveData))
    console.log('标准化后的保存数据:', normalizedData)

    let res
    if (currentTemplateId.value) {
      console.log('更新模板:', currentTemplateId.value)
      res = await templateApi.update(currentTemplateId.value, normalizedData)
    } else {
      console.log('创建新模板')
      res = await templateApi.create(normalizedData)
    }
      
    console.log('API响应:', res)
    
    if (res.status === 201 || res.status === 200) {
      // 更新本地状态
      const savedTemplate = res.data
      console.log('保存成功，返回的模板数据:', savedTemplate)
      
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
        console.log('刷新模板列表')
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
    console.error('保存模板失败:', error)
    
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
const handleLoadComplete = async ({ success, templateData: loadedTemplateData, profileData, error }) => {
  console.log('handleLoadComplete 被调用:', {
    success,
    mode: editorMode.value,
    hasProfileData: !!profileData,
    profileData
  })

  if (!success) {
    ElMessage.error(error || '加载失败')
    router.push('/')
    return
  }

  if (route.name === 'template-create') {
    // 初始化一个新的空模板
    updateCanvasData([{
      id: 0,
      elements: [],
      config: DEFAULT_CANVAS_CONFIG
    }])
    currentCanvasId.value = 0
  } else {
    // 确保我们使用正确的数据结构
    const templateToEdit = loadedTemplateData?.data || loadedTemplateData
    console.log('准备调用 handleEditTemplate，传入数据:', templateToEdit)
    
    // 如果是使用模式，将档案数据映射到模板
    if (editorMode.value === 'use' && profileData) {
      // 确保我们使用正确的档案数据结构
      const actualProfileData = profileData?.data?.data || profileData?.data || profileData
      console.log('使用模式，开始映射档案数据:', {
        actualProfileData,
        debugData: JSON.parse(localStorage.getItem('debug_profile_data'))
      })
      
      // 检查模板页面数据
      if (!templateToEdit.pages || !Array.isArray(templateToEdit.pages)) {
        console.error('模板缺少页面数据')
        ElMessage.error('模板数据格式不正确')
        return
      }

      // 映射档案数据到模板
      templateToEdit.pages = templateToEdit.pages.map((page, pageIndex) => {
        if (!page.page_data || !Array.isArray(page.page_data.elements)) {
          console.warn(`页面 ${pageIndex} 缺少元素数据:`, page)
          return page
        }

        console.log(`处理第 ${pageIndex + 1} 页的元素:`, page.page_data.elements)

        const elements = page.page_data.elements.map((element, elementIndex) => {
          // 只处理 resume-field 类型的元素
          if (element.type === 'resume-field' && element.props?.field) {
            console.log(`处理第 ${pageIndex + 1} 页的第 ${elementIndex + 1} 个元素:`, {
              type: element.type,
              field: element.props.field,
              currentContent: element.content
            })

            try {
              const fieldPath = element.props.field.split('.')
              let value = actualProfileData
              let currentPath = ''
              
              // 遍历字段路径获取值
              for (const key of fieldPath) {
                currentPath = currentPath ? `${currentPath}.${key}` : key
                value = value?.[key]
                console.log(`尝试获取字段 ${currentPath} 的值:`, value)
                if (value === undefined) break
              }

              // 如果找到值，更新元素内容
              if (value !== undefined && value !== null) {
                // 处理数组类型的值
                if (Array.isArray(value)) {
                  value = value.map(item => {
                    if (typeof item === 'object') {
                      return Object.values(item).join(' - ')
                    }
                    return String(item)
                  }).join('\n')
                } else if (typeof value === 'object') {
                  // 处理对象类型的值
                  value = Object.values(value).join(' - ')
                }

                console.log(`成功映射字段 ${element.props.field}:`, {
                  oldContent: element.content,
                  newContent: String(value)
                })
                return {
                  ...element,
                  content: String(value)
                }
              } else {
                console.warn(`未找到字段 ${element.props.field} 的值，保持原内容:`, element.content)
              }
            } catch (error) {
              console.error(`处理字段 ${element.props.field} 时出错:`, error)
            }
          } else {
            console.log(`跳过非 resume-field 元素:`, {
              type: element.type,
              content: element.content
            })
          }
          return element
        })

        return {
          ...page,
          page_data: {
            ...page.page_data,
            elements
          }
        }
      })
      
      console.log('映射档案数据后的模板:', templateToEdit)
    }
    
    handleEditTemplate(templateToEdit)
  }
  
  isLoading.value = false
}

// 修改 handleEditTemplate 方法
const handleEditTemplate = async (templateData) => {
  if (!templateData) {
    console.error('模板数据为空')
    ElMessage.error('模板数据加载失败')
    return
  }

  console.log('开始编辑模板:', templateData)
  currentTemplateId.value = templateData.id
  
  try {
    // 更新默认模板数据
    defaultTemplateData.value = {
      name: templateData.name || '',
      description: templateData.description || '',
      category: templateData.category || '',
      keywords: Array.isArray(templateData.keywords) ? templateData.keywords.join(',') : '',
      is_public: templateData.is_public ?? true,
      status: templateData.status || 0
    }

    // 构造新的画布数据
    const canvases = (templateData.pages || []).map((page, index) => {
      // 检查页面数据结构
      if (!page.page_data) {
        console.warn(`页面 ${index} 缺少 page_data，使用默认配置`)
        return {
          id: index,
          elements: [],
          config: { ...DEFAULT_CANVAS_CONFIG }
        }
      }

      // 处理元素数据
      const elements = (page.page_data.elements || []).map(element => {
        // 检查元素的必要属性
        if (!element.type) {
          console.warn('元素缺少类型信息:', element)
          return null
        }

        // 处理元素位置
        const position = element.position || {}
        const x = position.x ?? element.x ?? 0
        const y = position.y ?? element.y ?? 0

        // 处理元素样式
        const style = element.style || {}
        const transform = element.transform || {
          rotate: 0,
          scaleX: 1,
          scaleY: 1
        }

        return {
          id: element.id || `element-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          type: element.type,
          x,
          y,
          width: element.width || 100,
          height: element.height || 100,
          content: element.content || '',
          style,
          props: element.props || {},
          draggable: true,
          resizable: true,
          rotatable: true,
          lockAspectRatio: false,
          selected: false,
          zIndex: element.zIndex || 1,
          transform
        }
      }).filter(Boolean) // 过滤掉无效的元素

      // 处理画布配置
      const config = {
        width: page.page_data.config?.width || DEFAULT_CANVAS_CONFIG.width,
        height: page.page_data.config?.height || DEFAULT_CANVAS_CONFIG.height,
        backgroundColor: page.page_data.config?.backgroundColor || DEFAULT_CANVAS_CONFIG.backgroundColor,
        showGrid: page.page_data.config?.showGrid ?? DEFAULT_CANVAS_CONFIG.showGrid,
        showGuideLine: page.page_data.config?.showGuideLine ?? DEFAULT_CANVAS_CONFIG.showGuideLine,
        gridSize: page.page_data.config?.gridSize || DEFAULT_CANVAS_CONFIG.gridSize,
        gridColor: page.page_data.config?.gridColor || DEFAULT_CANVAS_CONFIG.gridColor
      }

      return {
        id: index,
        elements,
        config
      }
    })

    // 如果没有画布数据，创建一个默认画布
    if (canvases.length === 0) {
      canvases.push({
        id: 0,
        elements: [],
        config: { ...DEFAULT_CANVAS_CONFIG }
      })
    }

    // 更新画布数据
    updateCanvasData(canvases)
    currentCanvasId.value = 0

    console.log('模板加载完成:', {
      defaultTemplateData: defaultTemplateData.value,
      canvases,
      currentCanvasId: currentCanvasId.value
    })

  } catch (error) {
    console.error('处理模板数据时出错:', error)
    ElMessage.error('模板数据处理失败')
  }
} 