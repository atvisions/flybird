import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import { useStore } from 'vuex'

export function useEmail() {
  const store = useStore()
  const state = reactive({
    value: '',  // 邮箱地址
    code: '',   // 验证码
    password: '', // 添加密码字段
    loading: false,
    countdown: 0,
    sendingCode: false
  })

  // 发送验证码
  const handleSendCode = async () => {
    // 简单的邮箱格式验证
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(state.value)) {
      ElMessage.error('请输入正确的邮箱地址')
      return
    }

    try {
      state.sendingCode = true
      await request.post('/api/v1/users/account/send-email-code/', {
        email: state.value
      })
      
      ElMessage.success('验证码已发送')
      // 开始倒计时
      state.countdown = 60
      const timer = setInterval(() => {
        state.countdown--
        if (state.countdown <= 0) {
          clearInterval(timer)
        }
      }, 1000)
    } catch (error) {
      console.error('发送验证码失败:', error)
      ElMessage.error(error.response?.data?.detail || '发送验证码失败')
    } finally {
      state.sendingCode = false
    }
  }

  // 绑定邮箱
  const handleUpdate = async () => {
    if (!state.value || !state.code || (store.state.userInfo?.data?.user?.email && !state.password)) {
      ElMessage.error('请填写完整信息')
      return false
    }

    try {
      state.loading = true
      // 如果已有邮箱，使用更换邮箱接口
      const url = store.state.userInfo?.data?.user?.email 
        ? '/api/v1/users/account/change-email/'
        : '/api/v1/users/account/bind-email/'
      
      // 根据是否是更换邮箱发送不同的参数
      const data = store.state.userInfo?.data?.user?.email
        ? {
            email: state.value,
            code: state.code,
            password: state.password
          }
        : {
            email: state.value,
            code: state.code
          }
      
      await request.post(url, data)
      
      // 更新 store 中的用户信息
      await store.dispatch('fetchUserInfo')
      
      ElMessage.success(store.state.userInfo?.data?.user?.email ? '邮箱更换成功' : '邮箱绑定成功')
      return true
    } catch (error) {
      console.error('邮箱操作失败:', error)
      ElMessage.error(error.response?.data?.detail || '操作失败')
      return false
    } finally {
      state.loading = false
    }
  }

  return {
    state,
    handleSendCode,
    handleUpdate
  }
} 