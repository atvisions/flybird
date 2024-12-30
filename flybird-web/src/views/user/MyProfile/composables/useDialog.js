// src/views/user/MyProfile/composables/useDialog.js
import { ref } from 'vue'

export function useDialog() {
  const showEditModal = ref(false)
  const showAIModal = ref(false)
  const showCreationModal = ref(false)
  const aiSuggestions = ref([])
  const selectedCreationIds = ref([])

  const showAIOptimize = () => {
    showAIModal.value = true
  }

  const closeCreationModal = () => {
    showCreationModal.value = false
  }

  const handleAIAction = async (actionType, suggestion) => {
    // 实现 AI 操作逻辑
    console.log('AI Action:', actionType, suggestion)
  }
  return {
    showEditModal,
    showAIModal,
    showCreationModal,
    aiSuggestions,
    selectedCreationIds,
    showAIOptimize,
    closeCreationModal,
    handleAIAction
  }
}