import { reactive } from 'vue'

export function usePhone() {
  const state = reactive({
    value: '',  // 手机号
    code: '',   // 验证码
    loading: false,
    countdown: 0
  })

  return {
    state
  }
} 