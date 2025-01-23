// 判断模板是否可编辑
const isTemplateEditable = (template) => {
  const currentUserId = accountStore.userInfo?.id
  const isAdmin = accountStore.userInfo?.is_staff
  
  console.log('模板权限检查:', {
    templateId: template.id,
    templateCreator: template.creator,
    currentUserId: currentUserId,
    isAdmin: isAdmin,
    templateStatus: template.status,
    isMatch: template.creator === currentUserId
  })

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