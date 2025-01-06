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
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
            <ResumeCard
              v-for="template in filteredTemplates"
              :key="template.id"
              :template="{
                ...template,
                useCount: template.uses,
                viewCount: template.views,
                isPro: template.isPro
              }"
              @like="handleLike(template)"
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

// 模板数据
const templates = ref([
  {
    id: 1,
    title: '简约风格简历模板',
    description: '清新简约的设计风格，适合应届生和初级求职者使用...',
    cover: 'https://picsum.photos/600/800?random=1',
    category: '应届生',
    views: 1234,
    likes: 89,
    uses: 234,
    isPro: false,
    isLiked: false
  },
  {
    id: 2,
    title: '专业商务简历模板',
    description: '正式的商务风格设计，突出专业能力和工作经验...',
    cover: 'https://picsum.photos/600/800?random=2',
    category: '经验者',
    views: 856,
    likes: 67,
    uses: 156,
    isPro: true,
    isLiked: true
  },
  {
    id: 3,
    title: '创意设计师简历',
    description: '独特创意的设计风格，适合设计类岗位应聘...',
    cover: 'https://picsum.photos/600/800?random=3',
    category: '设计类',
    views: 2156,
    likes: 245,
    uses: 378,
    isPro: true,
    isLiked: false
  },
  {
    id: 4,
    title: '校园应届生简历',
    description: '突出学历和实习经验，适合应届生求职...',
    cover: 'https://picsum.photos/600/800?random=4',
    category: '应届生',
    views: 1567,
    likes: 123,
    uses: 289,
    isPro: false,
    isLiked: false
  },
  {
    id: 5,
    title: '高级工程师简历',
    description: '突出专业技能和项目经验，适合技术岗位...',
    cover: 'https://picsum.photos/600/800?random=5',
    category: '技术类',
    views: 3245,
    likes: 434,
    uses: 567,
    isPro: true,
    isLiked: false
  },
  {
    id: 6,
    title: '产品经理简历',
    description: '突出产品思维和项目管理能力...',
    cover: 'https://picsum.photos/600/800?random=6',
    category: '产品类',
    views: 2789,
    likes: 345,
    uses: 423,
    isPro: false,
    isLiked: false
  },
  {
    id: 7,
    title: '市场营销简历',
    description: '突出营销能力和业绩数据展示...',
    cover: 'https://picsum.photos/600/800?random=7',
    category: '市场类',
    views: 1890,
    likes: 234,
    uses: 345,
    isPro: true,
    isLiked: false
  },
  {
    id: 8,
    title: '实习生简历模板',
    description: '简洁大方，突出教育背景和实习意向...',
    cover: 'https://picsum.photos/600/800?random=8',
    category: '实习生',
    views: 2345,
    likes: 178,
    uses: 456,
    isPro: false,
    isLiked: false
  }
])

// 筛选逻辑
const filteredTemplates = computed(() => {
  if (currentCategory.value === 'all') {
    return templates.value
  }
  return templates.value.filter(template => template.category === currentCategory.value)
})

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

// 处理收藏
const handleLike = (template) => {
  template.isLiked = !template.isLiked
  // 这里可以添加收藏相关的API调用
}
</script> 