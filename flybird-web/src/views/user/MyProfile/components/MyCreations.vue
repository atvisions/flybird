<template>
  <div class="bg-white rounded-lg shadow">
    <!-- 标题栏和操作按钮 -->
    <div class="px-4 sm:px-6 py-4 border-b border-gray-200 flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-3 sm:space-y-0">
      <h3 class="text-lg font-medium text-gray-900">我的创作</h3>
      <div class="flex items-center space-x-3 self-end sm:self-auto">
        <button 
          @click="currentTab = 'drafts'"
          class="text-sm text-gray-600 hover:text-indigo-600 flex items-center"
        >
          <DocumentIcon class="w-4 h-4 mr-1" />
          草稿箱 ({{ drafts.length }})
        </button>
        <button 
          @click="handleCreate"
          class="inline-flex items-center px-3 py-1.5 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700"
        >
          <PlusIcon class="w-4 h-4 mr-1" />
          写文章
        </button>
      </div>
    </div>

    <!-- 内容标签页 -->
    <div class="p-2 sm:p-4">
      <!-- 标签切换 -->
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-4 sm:space-x-8 overflow-x-auto" aria-label="Tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="currentTab = tab.key"
            class="whitespace-nowrap py-3 px-2 sm:px-1 border-b-2 font-medium text-sm flex-shrink-0"
            :class="[
              currentTab === tab.key
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            {{ tab.label }}
            <span
              class="ml-1 sm:ml-2 rounded-full bg-gray-100 px-2 sm:px-2.5 py-0.5 text-xs font-medium text-gray-600"
            >{{ getCount(tab.key) }}</span>
          </button>
        </nav>
      </div>

      <!-- 内容区域 -->
      <div class="mt-4 overflow-x-hidden">
        <!-- 草稿箱 -->
        <div v-if="currentTab === 'drafts'" class="space-y-4">
          <div
            v-for="draft in drafts"
            :key="draft.id"
            class="p-3 sm:p-4 hover:bg-gray-50 rounded-lg transition-colors border border-gray-200"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h4 class="text-base font-medium text-gray-900">{{ draft.title || '无标题草稿' }}</h4>
                <p class="mt-1 text-sm text-gray-500">
                  最后编辑于 {{ draft.updateTime }}
                </p>
              </div>
              <div class="flex items-center space-x-2">
                <button 
                  @click="handleEdit(draft)"
                  class="p-1.5 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50"
                >
                  <PencilIcon class="w-4 h-4" />
                </button>
                <button 
                  @click="handleDelete(draft)"
                  class="p-1.5 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50"
                >
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 文章列表 -->
        <div v-if="currentTab === 'articles'" class="space-y-4">
          <div
            v-for="article in articles"
            :key="article.id"
            class="p-3 sm:p-4 hover:bg-gray-50 rounded-lg transition-colors border border-gray-200"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1 min-w-0">
                <h4 class="text-base font-medium text-gray-900 truncate group-hover:text-indigo-600">
                  {{ article.title }}
                </h4>
                <p class="mt-1 text-sm text-gray-500 line-clamp-2">
                  {{ article.description }}
                </p>
                <div class="mt-2 flex items-center text-xs text-gray-500 space-x-4">
                  <span>{{ article.createTime }}</span>
                  <span class="flex items-center">
                    <EyeIcon class="w-4 h-4 mr-1" />
                    {{ article.views }}
                  </span>
                  <span class="flex items-center">
                    <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />
                    {{ article.comments }}
                  </span>
                  <span class="flex items-center">
                    <HandThumbUpIcon class="w-4 h-4 mr-1" />
                    {{ article.likes }}
                  </span>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <button 
                  @click="handleEdit(article)"
                  class="p-1.5 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50"
                >
                  <PencilIcon class="w-4 h-4" />
                </button>
                <button 
                  @click="handleDelete(article)"
                  class="p-1.5 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50"
                >
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 问答列表 -->
        <div v-if="currentTab === 'questions'" class="space-y-4">
          <div
            v-for="question in questions"
            :key="question.id"
            class="p-4 hover:bg-gray-50 rounded-lg transition-colors"
          >
            <h4 class="text-base font-medium text-gray-900">
              {{ question.title }}
            </h4>
            <p class="mt-1 text-sm text-gray-500 line-clamp-2">
              {{ question.content }}
            </p>
            <div class="mt-2 flex items-center text-xs text-gray-500 space-x-4">
              <span>{{ question.createTime }}</span>
              <span>{{ question.answers }}个回答</span>
              <span class="flex items-center">
                <EyeIcon class="w-4 h-4 mr-1" />
                {{ question.views }}
              </span>
            </div>
          </div>
        </div>

        <!-- 话题列表 -->
        <div v-if="currentTab === 'topics'" class="space-y-4">
          <div
            v-for="topic in topics"
            :key="topic.id"
            class="p-4 hover:bg-gray-50 rounded-lg transition-colors"
          >
            <h4 class="text-base font-medium text-gray-900">
              {{ topic.title }}
            </h4>
            <div class="mt-3 flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center space-x-4">
                  <div class="flex-1">
                    <div class="flex justify-between mb-1">
                      <span class="text-sm text-gray-600">{{ topic.optionA }}</span>
                      <span class="text-sm text-gray-600">{{ topic.votesA }}票</span>
                    </div>
                    <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        class="h-full bg-blue-500 rounded-full"
                        :style="{ width: getVotePercentage(topic.votesA, topic.votesB) + '%' }"
                      ></div>
                    </div>
                  </div>
                  <span class="text-sm text-gray-500">VS</span>
                  <div class="flex-1">
                    <div class="flex justify-between mb-1">
                      <span class="text-sm text-gray-600">{{ topic.optionB }}</span>
                      <span class="text-sm text-gray-600">{{ topic.votesB }}票</span>
                    </div>
                    <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        class="h-full bg-indigo-500 rounded-full"
                        :style="{ width: getVotePercentage(topic.votesB, topic.votesA) + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-2 flex items-center text-xs text-gray-500 space-x-4">
              <span>{{ topic.createTime }}</span>
              <span>{{ topic.comments }}条评论</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <TransitionRoot appear :show="showDeleteDialog" as="template">
      <Dialog as="div" class="relative z-50" @close="closeDeleteDialog">
        <TransitionChild
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4">
            <TransitionChild
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                  确认删除
                </DialogTitle>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    {{ deleteItemType === 'draft' ? '确定要删除这个草稿吗？' : '确定要删除这篇内容吗？' }}
                    删除后将无法恢复。
                  </p>
                </div>

                <div class="mt-4 flex justify-end space-x-3">
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    @click="closeDeleteDialog"
                  >
                    取消
                  </button>
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
                    @click="confirmDelete"
                  >
                    确认删除
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import {
  EyeIcon,
  ChatBubbleLeftIcon,
  HandThumbUpIcon,
  PencilIcon,
  TrashIcon,
  PlusIcon,
  DocumentIcon
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'

const router = useRouter()

// 标签页配置
const tabs = [
  { key: 'articles', label: '文章' },
  { key: 'questions', label: '问答' },
  { key: 'topics', label: '话题' },
  { key: 'drafts', label: '草稿箱' }
]

const currentTab = ref('articles')

// 草稿数据
const drafts = ref([
  {
    id: 1,
    title: '前端性能优化实践',
    updateTime: '2024-01-15 14:30'
  }
])

// 删除相关状态
const showDeleteDialog = ref(false)
const deleteItemType = ref('')
const itemToDelete = ref(null)

// 处理删除
const handleDelete = (item) => {
  itemToDelete.value = item
  deleteItemType.value = currentTab.value === 'drafts' ? 'draft' : 'content'
  showDeleteDialog.value = true
}

// 关闭删除对话框
const closeDeleteDialog = () => {
  showDeleteDialog.value = false
  itemToDelete.value = null
}

// 确认删除
const confirmDelete = async () => {
  try {
    // TODO: 调用删除 API
    showToast('删除成功', 'success')
    closeDeleteDialog()
    // 重新加载数据
    await fetchData()
  } catch (error) {
    showToast('删除失败', 'error')
  }
}

// 处理编辑
const handleEdit = (item) => {
  if (currentTab.value === 'drafts') {
    router.push(`/editor/draft/${item.id}`)
  } else {
    router.push(`/editor/${currentTab.value}/${item.id}`)
  }
}

// 创建新文章
const handleCreate = () => {
  router.push('/editor/new')
}

// 获取各类型内容数量
const getCount = (type) => {
  switch (type) {
    case 'articles':
      return articles.value.length
    case 'questions':
      return questions.value.length
    case 'topics':
      return topics.value.length
    case 'drafts':
      return drafts.value.length
    default:
      return 0
  }
}

// 获取数据
const fetchData = async () => {
  try {
    // TODO: 调用相应的 API 获取数据
  } catch (error) {
    console.error('获取数据失败:', error)
    showToast('获取数据失败', 'error')
  }
}

// 在 script setup 中添加数据定义
const articles = ref([
  {
    id: 1,
    title: '2024年前端开发趋势展望',
    description: '探讨新的前端框架、工具和最佳实践，帮助开发者在新的一年保持技术领先。',
    createTime: '2小时前',
    views: 1234,
    comments: 56,
    likes: 89
  }
])

const questions = ref([
  {
    id: 1,
    title: 'Vue3性能优化的最佳实践有哪些？',
    content: '最近在做一个Vue3项目的性能优化，主要涉及到大数据列表渲染、组件懒加载等方面。想请教下大家在实际项目中都采用了哪些优化手段？',
    createTime: '4小时前',
    answers: 12,
    views: 892
  }
])

const topics = ref([
  {
    id: 1,
    title: '开发移动应用选择哪个方案？',
    optionA: 'Flutter',
    optionB: 'React Native',
    votesA: 234,
    votesB: 187,
    createTime: '1天前',
    comments: 89
  }
])

// 添加回投票百分比计算方法
const getVotePercentage = (votes, totalVotes) => {
  const total = votes + totalVotes
  return total === 0 ? 50 : Math.round((votes / total) * 100)
}
</script> 

<style scoped>
/* 隐藏滚动条但保持功能 */
.overflow-x-auto {
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.overflow-x-auto::-webkit-scrollbar {
  display: none; /* Chrome, Safari and Opera */
}
</style> 