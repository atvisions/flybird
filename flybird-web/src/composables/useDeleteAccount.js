import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'

export function useDeleteAccount() {
  const userStore = useUserStore()
  const authStore = useAuthStore()
  const deleteLoading = ref(false)

  return {
    deleteLoading,
    userStore,
    authStore
  }
} 