import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as templateApi from '@/api/template'

export const useTemplateStore = defineStore('template', () => {
  // 状态
  const categories = ref([])
  const templates = ref([])
  const currentTemplate = ref(null)
  const loading = ref(false)

  // 获取模板分类
  const getCategories = async () => {
    try {
      const response = await templateApi.getCategories()
      return response
    } catch (error) {
      console.error('获取分类失败:', error)
      throw error
    }
  }

  // 获取模板列表
  const getTemplates = async (params) => {
    loading.value = true
    try {
      const response = await templateApi.getTemplates(params)
      return response
    } catch (error) {
      console.error('获取模板列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取模板详情
  const getTemplateDetail = async (id) => {
    loading.value = true
    try {
      const response = await templateApi.getTemplateDetail(id)
      currentTemplate.value = response.data
      return currentTemplate.value
    } catch (error) {
      console.error('获取模板详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 保存模板
  const saveTemplate = async (templateData) => {
    loading.value = true
    try {
      const response = await templateApi.saveTemplate(templateData)
      return response.data
    } catch (error) {
      console.error('保存模板失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 更新模板
  const updateTemplate = async (id, templateData) => {
    loading.value = true
    try {
      const response = await templateApi.updateTemplate(id, templateData)
      return response.data
    } catch (error) {
      console.error('更新模板失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除模板
  const deleteTemplate = async (id) => {
    loading.value = true
    try {
      await templateApi.deleteTemplate(id)
      templates.value = templates.value.filter(template => template.id !== id)
    } catch (error) {
      console.error('删除模板失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 提交模板审核
  const submitForReview = async (id) => {
    loading.value = true
    try {
      const response = await templateApi.submitForReview(id)
      return response.data
    } catch (error) {
      console.error('提交模板审核失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    categories,
    templates,
    currentTemplate,
    loading,

    // 方法
    getCategories,
    getTemplates,
    getTemplateDetail,
    saveTemplate,
    updateTemplate,
    deleteTemplate,
    submitForReview
  }
}) 