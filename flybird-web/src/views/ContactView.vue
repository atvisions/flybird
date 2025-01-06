<template>
  <HeadView />
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-4xl font-bold text-gray-900 mb-8 text-center">联系我们</h1>
    
    <!-- 联系方式卡片 -->
    <div class="grid md:grid-cols-2 gap-8 mb-12">
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center space-x-4 mb-4">
          <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900">电子邮件</h3>
            <p class="text-gray-600">support@flybird.com</p>
            <p class="text-sm text-gray-500 mt-1">工作日 24 小时内回复</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center space-x-4 mb-4">
          <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900">客服热线</h3>
            <p class="text-gray-600">400-123-4567</p>
            <p class="text-sm text-gray-500 mt-1">周一至周五 9:00-18:00</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 留言表单 -->
    <div class="bg-white rounded-lg shadow-sm p-8">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">给我们留言</h2>
      <form class="space-y-6" @submit.prevent="handleSubmit">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">您的称呼</label>
          <input 
            type="text" 
            v-model="formData.name"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            required
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">联系方式</label>
          <input 
            type="text"
            v-model="formData.contact"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            required
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">留言内容</label>
          <textarea 
            rows="4"
            v-model="formData.message"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            required
          ></textarea>
        </div>
        <div>
          <button 
            type="submit"
            :disabled="isSubmitting"
            class="w-full bg-indigo-600 text-white px-6 py-3 rounded-md hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isSubmitting">提交中...</span>
            <span v-else>提交留言</span>
          </button>
        </div>
      </form>
    </div>
  </div>
  <FootView />
</template>

<script>
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'
import { ref } from 'vue'
import { showToast } from '@/components/ToastMessage'
import request from '@/utils/request'

export default {
  components: {
    HeadView,
    FootView
  },
  setup() {
    const formData = ref({
      name: '',
      contact: '',
      message: ''
    })
    
    const isSubmitting = ref(false)

    const handleSubmit = async () => {
      try {
        isSubmitting.value = true
        
        // 这里添加表单验证
        if (!formData.value.name.trim()) {
          showToast('请输入您的称呼', 'warning')
          return
        }
        
        if (!formData.value.contact.trim()) {
          showToast('请输入联系方式', 'warning')
          return
        }
        
        if (!formData.value.message.trim()) {
          showToast('请输入留言内容', 'warning')
          return
        }

        // 发送留言请求
        const response = await request({
          url: '/api/v1/feedback/submit/',
          method: 'post',
          data: formData.value
        })

        if (response.data?.code === 200) {
          showToast('留言提交成功，我们会尽快回复您', 'success')
          // 清空表单
          formData.value = {
            name: '',
            contact: '',
            message: ''
          }
        } else {
          throw new Error(response.data?.message || '提交失败')
        }
      } catch (error) {
        showToast(error.message || '提交失败，请稍后重试', 'error')
      } finally {
        isSubmitting.value = false
      }
    }

    return {
      formData,
      isSubmitting,
      handleSubmit
    }
  }
}
</script>