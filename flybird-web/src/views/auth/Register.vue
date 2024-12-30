const handleRegister = async () => {
  try {
    // 表单验证
    if (!form.value.phone) {
      showToast('请输入手机号', 'warning')
      return
    }
    if (!form.value.code) {
      showToast('请输入验证码', 'warning')
      return
    }
    if (!form.value.password) {
      showToast('请输入密码', 'warning')
      return
    }
    if (form.value.password.length < 6) {
      showToast('密码长度不能少于6位', 'warning')
      return
    }

    loading.value = true
    const response = await auth.register({
      phone: form.value.phone,
      code: form.value.code,
      password: form.value.password
    })

    if (response.data?.code === 200) {
      showToast('注册成功', 'success')
      // 清空表单
      form.value = {
        phone: '',
        code: '',
        password: ''
      }
      // 跳转到登录页
      router.push('/login')
    } else {
      throw new Error(response.data?.message || '注册失败')
    }
  } catch (error) {
    console.error('Register error:', error)
    const errorMessage = error.response?.data?.message 
      || error.response?.data?.errors?.phone?.[0]
      || error.response?.data?.errors?.code?.[0]
      || error.response?.data?.errors?.password?.[0]
      || error.message 
      || '注册失败，请稍后重试'
    showToast(errorMessage, 'error')
  } finally {
    loading.value = false
  }
} 