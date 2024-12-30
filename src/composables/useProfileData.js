const updateResumeData = async (data) => {
  try {
    const response = await updateBasicInfo(data)
    if (response.data.code === 200) {
      ElMessage.success('更新成功')
      return response.data.data
    }
    throw new Error(response.data.message)
  } catch (error) {
    console.error('更新用户资料失败:', error)
    
    // 处理验证错误
    if (error.response?.data?.errors) {
      const errors = error.response.data.errors
      // 显示第一个错误信息
      const firstError = Object.values(errors)[0]
      ElMessage.error(Array.isArray(firstError) ? firstError[0] : firstError)
    } else {
      // 显示一般错误
      ElMessage.error(error.response?.data?.message || '更新失败')
    }
    throw error
  }
} 