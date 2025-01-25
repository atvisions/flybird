// 判断模板是否可编辑
const isTemplateEditable = (template) => {
  const currentUserId = accountStore.userInfo?.id
  const isAdmin = accountStore.userInfo?.is_staff
  
  // 管理员可以编辑任何模板
  if (isAdmin) {
    return true
  }

  // 非管理员只能编辑自己创建的模板
  if (template.creator !== currentUserId) {
    return false
  }

  // 创建者可以修改任何状态的模板
  return true
}

const setup = () => {
  // 初始化状态
  onMounted(() => {
    loadCategories()
    loadTemplates()
  })
}

const loadCategories = async () => {
  try {
    const response = await categoryApi.getList()
    categoryList.value = response.data
  } catch (error) {
    categoryList.value = []
  }
}

const loadTemplates = async () => {
  loading.value = true
  try {
    const params = {}
    
    if (onlyMyTemplates.value) {
      if (!accountStore.userInfo?.id) {
        templates.value = []
        return
      }
      params.creator = accountStore.userInfo.id
    } else {
      params.status = 1
      params.is_public = true
      
      if (selectedCategory.value === 'recommended') {
        params.is_recommended = true
      } else if (selectedCategory.value) {
        params.category = selectedCategory.value
      }
    }
    
    params.sort = sortBy.value
    
    const response = await templateApi.getList(params)
    const templateList = response.data.results || []
    
    // 获取创建者信息
    const creatorIds = [...new Set(templateList.map(t => t.creator))]
    const creatorInfos = await Promise.all(
      creatorIds.map(id => userApi.getUserInfo(id))
    )
    
    // 处理模板数据
    templates.value = templateList.map(template => {
      const creatorInfo = creatorInfos.find(info => info.data.id === template.creator)?.data
      const avatarUrl = creatorInfo?.avatar || config.defaultAvatar
      
      return {
        ...template,
        creator_name: creatorInfo?.name || template.creator_name || '匿名用户',
        creator_avatar: avatarUrl,
        creator_is_vip: creatorInfo?.is_vip || false,
        creator_position: creatorInfo?.position || ''
      }
    })
  } catch (error) {
    showToast('获取模板列表失败', 'error')
    templates.value = []
  } finally {
    loading.value = false
  }
} 