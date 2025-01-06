// src/views/user/MyProfile/composables/useLoading.js
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export function useLoading() {
  const loading = ref(false)

  const withLoading = async (fn) => {
    try {
      loading.value = true
      await fn()
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    withLoading
  }
}