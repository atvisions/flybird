<template>
    <div class="space-y-4">
      <!-- 简历列表 -->
      <div v-for="resume in resumes" :key="resume.id" 
        class="bg-white rounded-lg border hover:shadow-sm transition-shadow duration-300">
        <div class="p-4">
          <!-- 标题栏 -->
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center space-x-2">
              <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-900">{{ resume.title }}</h3>
                <p class="text-xs text-gray-500">更新于 {{ formatDate(resume.updatedAt) }}</p>
              </div>
            </div>
            <div class="text-xs text-gray-500">
              {{ resume.template.name }} | {{ resume.language === 'zh' ? '中文' : 'English' }}
            </div>
          </div>
  
          <!-- 操作按钮组 -->
          <div class="flex items-center space-x-2 mt-4">
            <button @click="handleEdit(resume)"
              class="inline-flex items-center px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border rounded-md hover:bg-gray-50">
              <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              编辑
            </button>
            <button @click="handlePreview(resume)"
              class="inline-flex items-center px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border rounded-md hover:bg-gray-50">
              <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              预览
            </button>
            <button @click="handleExport(resume)"
              class="inline-flex items-center px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border rounded-md hover:bg-gray-50">
              <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              导出 PDF
            </button>
            <button @click="handleDelete(resume)"
              class="inline-flex items-center px-3 py-1.5 text-xs font-medium text-red-600 bg-white border rounded-md hover:bg-red-50">
              <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              删除
            </button>
          </div>
  
          <!-- 简历信息 -->
          <div class="flex items-center space-x-4 mt-3 text-xs text-gray-500">
            <div class="flex items-center">
              <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              {{ resume.name }} | {{ resume.expectedPosition }}
            </div>
            <div class="flex items-center">
              <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              {{ resume.workYears }}
            </div>
            <div class="flex items-center">
              <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ resume.expectedSalary }}
            </div>
          </div>
        </div>
      </div>
  
      <!-- 创建简历按钮 -->
      <button @click="handleCreateResume"
        class="w-full p-4 text-sm text-gray-500 border border-dashed rounded-lg hover:border-gray-400 hover:text-gray-600 transition-colors duration-300 flex items-center justify-center">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        创建新简历
      </button>
    </div>
  </template>
  
  <script setup>
  /* eslint-disable no-unused-vars */
  import { ref, onMounted, onUnmounted } from 'vue'
  
  // 当前打开的菜单
  const activeMenu = ref(null)
  
  // 模拟简历数据
  const resumes = ref([
    {
      id: 1,
      title: '产品设计师简历',
      name: '张三',
      expectedPosition: '高级产品设计师',
      workYears: '5年',
      expectedSalary: '25-35K',
      completeness: 85,
      createdAt: '2024-03-01T10:00:00',
      updatedAt: '2024-03-15T10:00:00',
      template: {
        id: 1,
        name: '简约商务',
        cover: 'https://images.unsplash.com/photo-1586281380349-632531db7ed4?q=80&w=300&h=400&fit=crop',
        description: '适合商务人士的专业简历模板',
        category: 'business',
        language: ['zh', 'en'],
        color: ['blue', 'black', 'gray']
      },
      language: 'zh'
    },
    {
      id: 2,
      title: 'UI Designer Resume',
      name: '张三',
      expectedPosition: 'Senior UI Designer',
      workYears: '5年',
      expectedSalary: '20-30K',
      completeness: 90,
      createdAt: '2024-02-15T14:30:00',
      updatedAt: '2024-03-10T14:30:00',
      template: {
        id: 2,
        name: 'Modern Creative',
        cover: 'https://images.unsplash.com/photo-1586281380117-5a60ae2050cc?q=80&w=300&h=400&fit=crop',
        description: '富有创意的现代简历模板',
        category: 'creative',
        language: ['en', 'zh'],
        color: ['purple', 'green', 'orange']
      },
      language: 'en'
    }
  ])
  
  // 格式化日期
  const formatDate = (date) => {
    const d = new Date(date)
    return `${d.getMonth() + 1}月${d.getDate()}日`
  }
  
  // 切换菜单显示
  const toggleMenu = (id) => {
    activeMenu.value = activeMenu.value === id ? null : id
  }
  
  // 创建新简历
  const handleCreateResume = () => {
    // TODO: 跳转到简历编辑页面
    console.log('创建新简历')
  }
  
  // 编辑简历
  const handleEdit = (resume) => {
    // TODO: 跳转到简历编辑页面
    console.log('编辑简历:', resume.id)
    activeMenu.value = null
  }
  
  // 预览简历
  const handlePreview = (resume) => {
    // TODO: 打开简历预览
    console.log('预览简历:', resume.id)
    activeMenu.value = null
  }
  
  // 导出PDF
  const handleExport = (resume) => {
    // TODO: 导出PDF
    console.log('导出简历:', resume.id)
    activeMenu.value = null
  }
  
  // 删除简历
  const handleDelete = (resume) => {
    // TODO: 确认删除
    console.log('删除简历:', resume.id)
    activeMenu.value = null
  }
  
  // 点击其他地方关闭菜单
  const closeMenu = (e) => {
    if (!e.target.closest('.relative')) {
      activeMenu.value = null
    }
  }
  
  // 添加全局点击事件监听
  onMounted(() => {
    document.addEventListener('click', closeMenu)
  })
  
  onUnmounted(() => {
    document.removeEventListener('click', closeMenu)
  })
  </script>
  
  <style scoped>
  /* 添加一些过渡效果 */
  .hover\:shadow-md {
    transition: all 0.3s ease;
  }
  
  /* 给封面图片添加渐变遮罩 */
  .object-cover {
    position: relative;
  }
  
  .object-cover::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0.02), rgba(0,0,0,0.1));
    pointer-events: none;
  }
  </style>