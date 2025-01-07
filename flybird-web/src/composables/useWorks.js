import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

export function useWorks(type) {
  const works = ref([])
  const loading = ref(false)
  const error = ref(null)
  const api = useApi()

  const fetchWorks = async () => {
    loading.value = true
    try {
      const response = await api.get(`/works/${type}`)
      works.value = response.data
    } catch (err) {
      error.value = err
    } finally {
      loading.value = false
    }
  }

  onMounted(fetchWorks)

  return {
    works,
    loading,
    error,
    fetchWorks
  }
} 