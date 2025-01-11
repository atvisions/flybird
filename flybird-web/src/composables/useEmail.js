import { reactive } from 'vue'

export function useEmail() {
  const state = reactive({
    value: '',        // 邮箱值
    code: '',         // 验证码
    password: '',     // 密码
    loading: false,   // 加载状态
    countdown: 0      // 倒计时
  })

  return {
    state
  }
} 