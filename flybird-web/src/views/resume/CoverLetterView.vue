<template>
  <div class="py-4 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <PageBanner theme="rose">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">{{ getCurrentNavName }}</h1>
        <p class="text-gray-600 text-lg max-w-2xl">{{ getBannerDescription }}</p>
      </PageBanner>

      <TemplateNavigation v-model:currentCategory="currentCategory" />

      <!-- 模板列表 -->
      <div class="mt-3 md:mt-6">
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2 md:gap-6">
          <TemplateCard
            v-for="template in filteredTemplates"
            :key="template.id"
            :template="template"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import TemplateCard from '@/components/resume/ResumeCard.vue'
import PageBanner from '@/components/common/PageBanner.vue'
import TemplateNavigation from '@/components/resume/TemplateNavigation.vue'

const route = useRoute()
const currentCategory = ref('all')
const currentSort = ref('popular')

const templates = ref([
  // 求职信模板数据
])

const filteredTemplates = computed(() => templates.value)

// 获取当前导航名称
const getCurrentNavName = computed(() => {
  const navMap = {
    '/templates': '全部模板',
    '/templates/resume': '简历模板',
    '/templates/cover-letter': '求职信',
    '/templates/bio': '个人简介'
  }
  return navMap[route.path] || '全部模板'
})

// 获取横幅描述
const getBannerDescription = computed(() => {
  const descriptions = {
    '/templates': '精选优质简历模板，助你打造完美简历',
    '/templates/resume': '为在校生和应届生量身定制的简历模板',
    '/templates/cover-letter': '专业的求职信模板，助力职业发展',
    '/templates/bio': '专业的个人简介模板，展现个人魅力'
  }
  return descriptions[route.path] || ''
})
</script> 