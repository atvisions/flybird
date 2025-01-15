import { ElMessage } from 'element-plus'

export const showToast = (message, type = 'info') => {
  ElMessage({
    message,
    type,
    duration: 3000,
    showClose: true,
    center: true
  })
} 