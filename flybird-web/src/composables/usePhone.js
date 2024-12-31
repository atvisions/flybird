import { reactive } from 'vue'
import { useStore } from 'vuex'
import { user } from '@/api/user'
import { auth } from '@/api/auth'
import { SMS_SCENE } from '@/constants'
import { showToast } from '@/components/ToastMessage'

export function usePhone() {
  const store = useStore()
  const state = reactive({
    value: '',
    code: '',
    loading: false,
    countdown: 0
  })

  const handleSendCode = async () => {
    if (!/^1[3-9]\d{9}$/.test(state.value)) {
      showToast('请输入正确的手机号', 'error')
      return
    }

    state.loading = true
    try {
      await auth.sendVerifyCode({
        phone: state.value,
        scene: SMS_SCENE.CHANGE_PHONE
      })
      showToast('验证码已发送', 'success')
      state.countdown = 60
      const timer = setInterval(() => {
        state.countdown--
        if (state.countdown <= 0) {
          clearInterval(timer)
        }
      }, 1000)
    } catch (error) {
      showToast(error.response?.data?.message || '发送失败', 'error')
    } finally {
      state.loading = false
    }
  }

  const handleUpdate = async () => {
    if (!state.value.trim() || !state.code.trim()) {
      showToast('请输入手机号和验证码', 'error')
      return false
    }

    state.loading = true
    try {
      await user.changePhone({
        phone: state.value,
        code: state.code
      })
      await store.dispatch('fetchUserInfo')
      showToast('手机号修改成功', 'success')
      return true
    } catch (error) {
      showToast(error.message || '修改失败', 'error')
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