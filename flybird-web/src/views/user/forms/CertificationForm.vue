<template>
    <div class="space-y-6">
      <!-- 证书列表 -->
      <TransitionGroup name="list" tag="div" class="space-y-4">
        <div
          v-for="(cert, index) in certifications"
          :key="cert.id"
          class="relative flex items-center space-x-3 bg-gray-50 p-4 rounded-lg"
        >
          <!-- 证书图标 -->
          <div class="flex-shrink-0">
            <div class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
              <svg class="h-6 w-6 text-indigo-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M11.7 2.805a.75.75 0 01.6 0A60.65 60.65 0 0122.83 8.72a.75.75 0 01-.231 1.337 49.949 49.949 0 00-9.902 3.912l-.003.002-.34.18a.75.75 0 01-.707 0A50.009 50.009 0 007.5 12.174v-.224c0-.131.067-.248.172-.311a54.614 54.614 0 014.653-2.52.75.75 0 00-.65-1.352 56.129 56.129 0 00-4.78 2.589 1.858 1.858 0 00-.859 1.228 49.803 49.803 0 00-4.634-1.527.75.75 0 01-.231-1.337A60.653 60.653 0 0111.7 2.805z" />
              </svg>
            </div>
          </div>
  
          <!-- 证书信息 -->
          <div class="min-w-0 flex-1">
            <div class="text-sm font-medium text-gray-900">{{ cert.name }}</div>
            <div class="text-sm text-gray-500">
              <span>颁发机构：{{ cert.issuer }}</span>
              <span class="mx-2">·</span>
              <span>获得时间：{{ cert.date }}</span>
            </div>
          </div>
  
          <!-- 操作按钮 -->
          <div class="flex-shrink-0">
            <button
              @click="removeCertification(index)"
              class="inline-flex items-center p-1 border border-transparent rounded-full text-gray-400 hover:text-gray-500"
            >
              <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
              </svg>
            </button>
          </div>
        </div>
      </TransitionGroup>
  
      <!-- 添加证书表单 -->
      <div v-if="showForm" class="border rounded-lg p-4">
        <div class="space-y-4">
          <div>
            <label for="certName" class="block text-sm font-medium text-gray-700">证书名称</label>
            <input
              type="text"
              id="certName"
              v-model="newCert.name"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
          <div>
            <label for="certIssuer" class="block text-sm font-medium text-gray-700">颁发机构</label>
            <input
              type="text"
              id="certIssuer"
              v-model="newCert.issuer"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
          <div>
            <label for="certDate" class="block text-sm font-medium text-gray-700">获得时间</label>
            <input
              type="date"
              id="certDate"
              v-model="newCert.date"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button
              @click="cancelAdd"
              class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              取消
            </button>
            <button
              @click="addCertification"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              添加
            </button>
          </div>
        </div>
      </div>
  
      <!-- 添加按钮 -->
      <button
        v-if="!showForm"
        @click="showForm = true"
        class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        <svg class="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path d="M10.75 4.75a.75.75 0 00-1.5 0v4.5h-4.5a.75.75 0 000 1.5h4.5v4.5a.75.75 0 001.5 0v-4.5h4.5a.75.75 0 000-1.5h-4.5v-4.5z" />
        </svg>
        添加证书
      </button>
  
      <!-- 保存按钮 -->
      <div class="flex justify-end pt-6">
        <button
          @click="save"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          保存
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const emit = defineEmits(['saved'])
  
  // 证书列表
  const certifications = ref([])
  
  // 新证书表单
  const showForm = ref(false)
  const newCert = ref({
    name: '',
    issuer: '',
    date: ''
  })
  
  // 添加证书
  const addCertification = () => {
    if (newCert.value.name && newCert.value.issuer && newCert.value.date) {
      certifications.value.push({
        id: Date.now(),
        ...newCert.value
      })
      // 重置表单
      newCert.value = {
        name: '',
        issuer: '',
        date: ''
      }
      showForm.value = false
    }
  }
  
  // 取消添加
  const cancelAdd = () => {
    newCert.value = {
      name: '',
      issuer: '',
      date: ''
    }
    showForm.value = false
  }
  
  // 移除证书
  const removeCertification = (index) => {
    certifications.value.splice(index, 1)
  }
  
  // 保存
  const save = () => {
    // TODO: 调用 API 保存数据
    emit('saved')
  }
  </script>
  
  <style scoped>
  .list-enter-active,
  .list-leave-active {
    transition: all 0.3s ease;
  }
  
  .list-enter-from,
  .list-leave-to {
    opacity: 0;
    transform: translateY(-30px);
  }
  </style>