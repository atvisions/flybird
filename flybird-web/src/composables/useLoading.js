import { ref } from 'vue'

// 方式一：默认导出
export default function useLoading() {
  const loading = ref(false)

  // 包装异步函数，自动处理 loading 状态
  const withLoading = async (fn) => {
    try {
      loading.value = true
      return await fn()
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    withLoading
  }
}

// 或者方式二：命名导出
// export const useLoading = () => {
//   const loading = ref(false)
//
//   const withLoading = async (fn) => {
//     try {
//       loading.value = true
//       return await fn()
//     } finally {
//       loading.value = false
//     }
//   }
//
//   return {
//     loading,
//     withLoading
//   }
// } 