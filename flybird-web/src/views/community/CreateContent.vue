<template>
  <div class="min-h-screen py-4 pb-24 lg:py-6 mt-[72px]">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 内容类型选择 -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6 mb-6">
        <div class="flex items-center gap-4">
          <button
            v-for="type in contentTypes"
            :key="type.id"
            class="flex-1 h-20 rounded-lg border-2 transition-colors flex flex-col items-center justify-center gap-2"
            :class="[
              selectedType === type.id 
                ? 'border-violet-600 bg-violet-50 text-violet-600' 
                : 'border-gray-200 hover:border-violet-200'
            ]"
            @click="selectedType = type.id"
          >
            <component :is="type.icon" class="w-6 h-6" />
            <span class="text-sm font-medium">{{ type.name }}</span>
          </button>
        </div>
      </div>

      

      <!-- 文章发布表单 -->
      <div v-if="selectedType === 'article'" class="relative bg-white rounded-xl border border-gray-100">
        <ArticleForm />
      </div>
      <!-- 话题发布表单 -->
      <div v-if="selectedType === 'topic'" class="bg-white rounded-xl border border-gray-100">
        <div class="space-y-6 p-4 lg:p-6 pb-24">
          <!-- 话题主题 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">话题主题</label>
            <input
              type="text"
              v-model="topicForm.title"
              class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
              placeholder="例如：Vue 和 React，哪个更适合新手入门？"
            >
          </div>

          <!-- 话题分类 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">话题分类</label>
            <Listbox v-model="selectedTopicCategory">
              <div class="relative">
                <ListboxButton
                  class="relative w-full cursor-pointer rounded-lg bg-white py-2.5 pl-3 pr-10 text-left border border-gray-300 focus:outline-none focus:ring-2 focus:ring-violet-500 sm:text-sm"
                >
                  <span class="flex items-center">
                    <component 
                      :is="selectedTopicCategory.icon" 
                      class="h-5 w-5 flex-shrink-0 text-gray-400"
                      aria-hidden="true"
                    />
                    <span class="ml-3 block truncate">{{ selectedTopicCategory.name }}</span>
                  </span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                </ListboxButton>

                <Transition
                  leave-active-class="transition duration-100 ease-in"
                  leave-from-class="opacity-100"
                  leave-to-class="opacity-0"
                >
                  <ListboxOptions
                    class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                  >
                    <ListboxOption
                      v-for="category in categories"
                      :key="category.id"
                      :value="category"
                      v-slot="{ active, selected }"
                      as="template"
                    >
                      <li
                        :class="[
                          active ? 'bg-violet-600 text-white' : 'text-gray-900',
                          'relative cursor-pointer select-none py-2 pl-3 pr-9'
                        ]"
                      >
                        <div class="flex items-center">
                          <component 
                            :is="category.icon" 
                            :class="[
                              active ? 'text-white' : 'text-gray-400',
                              'h-5 w-5 flex-shrink-0'
                            ]"
                            aria-hidden="true"
                          />
                          <span
                            :class="[
                              selected ? 'font-semibold' : 'font-normal',
                              'ml-3 block truncate'
                            ]"
                          >
                            {{ category.name }}
                          </span>
                        </div>

                        <span
                          v-if="selected"
                          :class="[
                            active ? 'text-white' : 'text-violet-600',
                            'absolute inset-y-0 right-0 flex items-center pr-4'
                          ]"
                        >
                          <CheckIcon class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ListboxOption>
                  </ListboxOptions>
                </Transition>
              </div>
            </Listbox>
          </div>

          <!-- 投票选项 -->
          <div class="space-y-4">
            <label class="block text-sm font-medium text-gray-700">投票选项</label>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs text-gray-500 mb-1.5">选项 A</label>
                <input
                  type="text"
                  v-model="topicForm.optionA"
                  class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
                  placeholder="例如：Vue"
                >
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1.5">选项 B</label>
                <input
                  type="text"
                  v-model="topicForm.optionB"
                  class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
                  placeholder="例如：React"
                >
              </div>
            </div>
          </div>

          <!-- 话题描述 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">话题描述</label>
            <textarea
              v-model="topicForm.content"
              rows="6"
              class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
              placeholder="详细描述这个话题，可以分析两个选项的优劣势..."
            ></textarea>
          </div>

          <!-- 标签 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">添加标签</label>
            <div class="flex flex-wrap gap-2">
              <div
                v-for="tag in topicForm.tags"
                :key="tag"
                class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm flex items-center group"
              >
                <span>{{ tag }}</span>
                <XMarkIcon 
                  class="w-4 h-4 ml-1 cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity"
                  @click="removeTopicTag(tag)"
                />
              </div>
              <input
                v-if="topicForm.tags.length < 5"
                type="text"
                v-model="newTopicTag"
                @keydown.enter="addTopicTag"
                class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
                placeholder="按回车添加标签"
              >
            </div>
            <p class="mt-1 text-xs text-gray-500">最多添加 5 个标签</p>
          </div>
        </div>

        <!-- 固定的底部按钮区域 -->
        <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-4 z-50">
          <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-500">已自动保存草稿</span>
              <div class="flex items-center gap-4">
                <button 
                  class="px-6 h-10 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors"
                  @click="$router.back()"
                >
                  取消
                </button>
                <button 
                  class="px-6 h-10 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
                  @click="submitTopic"
                >
                  发布话题
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 问答发布表单 -->
      <div v-else-if="selectedType === 'question'" class="bg-white rounded-xl border border-gray-100">
        <div class="space-y-6 p-4 lg:p-6 pb-24">
          <!-- 标题 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">问题标题</label>
            <input
              type="text"
              v-model="questionForm.title"
              class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
              placeholder="一句话描述你的问题"
            >
          </div>

          <!-- 问题类型和分类 -->
          <div class="grid grid-cols-2 gap-4">
            <!-- 问题类型 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">问题类型</label>
              <Listbox v-model="questionForm.type">
                <div class="relative">
                  <ListboxButton
                    class="relative w-full cursor-pointer rounded-lg bg-white py-2.5 pl-3 pr-10 text-left border border-gray-300 focus:outline-none focus:ring-2 focus:ring-violet-500 sm:text-sm"
                  >
                    <span class="flex items-center">
                      <component 
                        :is="questionTypes[questionForm.type].icon" 
                        class="h-5 w-5 flex-shrink-0 text-gray-400"
                        aria-hidden="true"
                      />
                      <span class="ml-3 block truncate">{{ questionTypes[questionForm.type].name }}</span>
                    </span>
                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                    </span>
                  </ListboxButton>

                  <Transition
                    leave-active-class="transition duration-100 ease-in"
                    leave-from-class="opacity-100"
                    leave-to-class="opacity-0"
                  >
                    <ListboxOptions
                      class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                    >
                      <ListboxOption
                        v-for="(type, key) in questionTypes"
                        :key="key"
                        :value="key"
                        v-slot="{ active, selected }"
                        as="template"
                      >
                        <li
                          :class="[
                            active ? 'bg-violet-600 text-white' : 'text-gray-900',
                            'relative cursor-pointer select-none py-2 pl-3 pr-9'
                          ]"
                        >
                          <div class="flex items-center">
                            <component 
                              :is="type.icon" 
                              :class="[
                                active ? 'text-white' : 'text-gray-400',
                                'h-5 w-5 flex-shrink-0'
                              ]"
                              aria-hidden="true"
                            />
                            <span
                              :class="[
                                selected ? 'font-semibold' : 'font-normal',
                                'ml-3 block truncate'
                              ]"
                            >
                              {{ type.name }}
                            </span>
                          </div>

                          <span
                            v-if="selected"
                            :class="[
                              active ? 'text-white' : 'text-violet-600',
                              'absolute inset-y-0 right-0 flex items-center pr-4'
                            ]"
                          >
                            <CheckIcon class="h-5 w-5" aria-hidden="true" />
                          </span>
                        </li>
                      </ListboxOption>
                    </ListboxOptions>
                  </Transition>
                </div>
              </Listbox>
            </div>

            <!-- 问题分类 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">问题分类</label>
              <Listbox v-model="selectedCategory">
                <div class="relative">
                  <ListboxButton
                    class="relative w-full cursor-pointer rounded-lg bg-white py-2.5 pl-3 pr-10 text-left border border-gray-300 focus:outline-none focus:ring-2 focus:ring-violet-500 sm:text-sm"
                  >
                    <span class="flex items-center">
                      <component 
                        :is="selectedCategory.icon" 
                        class="h-5 w-5 flex-shrink-0 text-gray-400"
                        aria-hidden="true"
                      />
                      <span class="ml-3 block truncate">{{ selectedCategory.name }}</span>
                    </span>
                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                    </span>
                  </ListboxButton>

                  <Transition
                    leave-active-class="transition duration-100 ease-in"
                    leave-from-class="opacity-100"
                    leave-to-class="opacity-0"
                  >
                    <ListboxOptions
                      class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                    >
                      <ListboxOption
                        v-for="category in categories"
                        :key="category.id"
                        :value="category"
                        v-slot="{ active, selected }"
                        as="template"
                      >
                        <li
                          :class="[
                            active ? 'bg-violet-600 text-white' : 'text-gray-900',
                            'relative cursor-pointer select-none py-2 pl-3 pr-9'
                          ]"
                        >
                          <div class="flex items-center">
                            <component 
                              :is="category.icon" 
                              :class="[
                                active ? 'text-white' : 'text-gray-400',
                                'h-5 w-5 flex-shrink-0'
                              ]"
                              aria-hidden="true"
                            />
                            <span
                              :class="[
                                selected ? 'font-semibold' : 'font-normal',
                                'ml-3 block truncate'
                              ]"
                            >
                              {{ category.name }}
                            </span>
                          </div>

                          <span
                            v-if="selected"
                            :class="[
                              active ? 'text-white' : 'text-violet-600',
                              'absolute inset-y-0 right-0 flex items-center pr-4'
                            ]"
                          >
                            <CheckIcon class="h-5 w-5" aria-hidden="true" />
                          </span>
                        </li>
                      </ListboxOption>
                    </ListboxOptions>
                  </Transition>
                </div>
              </Listbox>
            </div>
          </div>

          <!-- 悬赏设置 -->
          <div v-if="questionForm.type === 'bounty'" class="space-y-4">
            <label class="block text-sm font-medium text-gray-700">悬赏设置</label>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs text-gray-500 mb-1.5">悬赏金额</label>
                <div class="relative">
                  <input
                    type="number"
                    v-model="questionForm.bounty"
                    class="block w-full rounded-lg border-gray-300 pl-6 shadow-sm focus:border-violet-500 focus:ring-violet-500"
                    placeholder="输入金额"
                    min="1"
                  >
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">¥</span>
                </div>
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1.5">悬赏时间</label>
                <Listbox
                  v-model="questionForm.bountyDays"
                >
                  <div class="relative">
                    <ListboxButton
                      class="relative w-full cursor-pointer rounded-lg bg-white py-2.5 pl-3 pr-10 text-left border border-gray-300 focus:outline-none focus:ring-2 focus:ring-violet-500 sm:text-sm"
                    >
                      <span class="block truncate">{{ questionForm.bountyDays }}天</span>
                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </ListboxButton>
                    <Transition
                      leave-active-class="transition duration-100 ease-in"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <ListboxOptions
                        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                      >
                        <ListboxOption
                          v-for="days in bountyDaysOptions"
                          :key="days"
                          :value="days"
                          v-slot="{ active, selected }"
                          as="template"
                        >
                          <li
                            :class="[
                              active ? 'bg-violet-600 text-white' : 'text-gray-900',
                              'relative cursor-pointer select-none py-2 pl-3 pr-9'
                            ]"
                          >
                            <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                              {{ days }}天
                            </span>
                            <span
                              v-if="selected"
                              :class="[
                                active ? 'text-white' : 'text-violet-600',
                                'absolute inset-y-0 right-0 flex items-center pr-4'
                              ]"
                            >
                              <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </Transition>
                  </div>
                </Listbox>
              </div>
            </div>
            <p class="text-xs text-gray-500">
              悬赏问题会获得更多关注，悬赏金额将在采纳答案后支付给回答者
            </p>
          </div>

          <!-- 问题描述 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">问题描述</label>
            <textarea
              v-model="questionForm.content"
              rows="6"
              class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
              placeholder="详细描述你的问题，以便他人更好地帮助你"
            ></textarea>
          </div>

          <!-- 标签 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">添加标签</label>
            <div class="flex flex-wrap gap-2">
              <div
                v-for="tag in questionForm.tags"
                :key="tag"
                class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm flex items-center group"
              >
                <span>{{ tag }}</span>
                <XMarkIcon 
                  class="w-4 h-4 ml-1 cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity"
                  @click="removeTag(tag)"
                />
              </div>
              <input
                v-if="questionForm.tags.length < 5"
                type="text"
                v-model="newTag"
                @keydown.enter="addTag"
                class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
                placeholder="按回车添加标签"
              >
            </div>
            <p class="mt-1 text-xs text-gray-500">最多添加 5 个标签</p>
          </div>
        </div>

        <!-- 固定的底部按钮区域 -->
        <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-4 z-50">
          <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-500">已自动保存草稿</span>
              <div class="flex items-center gap-4">
                <button 
                  class="px-6 h-10 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors"
                  @click="$router.back()"
                >
                  取消
                </button>
                <button 
                  class="px-6 h-10 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
                  @click="submitQuestion"
                >
                  发布问题
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  DocumentTextIcon,
  QuestionMarkCircleIcon,
  HashtagIcon,
  XMarkIcon,
  ChevronUpDownIcon,
  CheckIcon,
  CurrencyYenIcon,
  ChatBubbleLeftRightIcon,
  CodeBracketIcon,
  ServerIcon,
  DevicePhoneMobileIcon,
  ChartBarIcon,
  DatabaseIcon,
  CpuChipIcon,
  BeakerIcon
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'
import ArticleForm from './components/ArticleForm.vue'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'

const router = useRouter()
const route = useRoute()

// 文章表单数据
const articleForm = ref({
  title: '',
  category: '',
  content: '',
  tags: [],
  cover: '',
  summary: '',
  isPublic: true,
  allowComment: true
})

// 内容类型
const contentTypes = [
  { id: 'article', name: '发布文章', icon: DocumentTextIcon },
  { id: 'topic', name: '发起话题', icon: HashtagIcon },
  { id: 'question', name: '发布问题', icon: QuestionMarkCircleIcon },
]

// 根据来源页面设置默认类型
const getDefaultType = () => {
  // 从查询参数获取类型
  const type = route.query.type
  // 检查是否是有效的类型
  if (contentTypes.some(t => t.id === type)) {
    return type
  }
  // 默认返回文章类型
  return 'article'
}

const selectedType = ref(getDefaultType())

// 问题类型定义
const questionTypes = {
  normal: {
    name: '普通提问',
    icon: QuestionMarkCircleIcon,
    description: '寻求技术解答和建议'
  },
  bounty: {
    name: '悬赏问答',
    icon: CurrencyYenIcon,
    description: '通过悬赏获得更快解答'
  },
  discussion: {
    name: '技术讨论',
    icon: ChatBubbleLeftRightIcon,
    description: '发起技术话题讨论'
  }
}

// 分类数据
const categories = [
  { id: 'frontend', name: '前端开发', icon: CodeBracketIcon },
  { id: 'backend', name: '后端开发', icon: ServerIcon },
  { id: 'mobile', name: '移动开发', icon: DevicePhoneMobileIcon },
  { id: 'algorithm', name: '算法', icon: ChartBarIcon },
  { id: 'database', name: '数据库', icon: DatabaseIcon },
  { id: 'devops', name: '运维', icon: CpuChipIcon },
  { id: 'ai', name: '人工智能', icon: BeakerIcon }
]

// 选中的分类
const selectedCategory = ref(categories[0])

// 悬赏时间选项
const bountyDaysOptions = [3, 7, 15, 30]

// 问答表单数据
const questionForm = ref({
  title: '',
  type: 'normal',
  category: '',
  bounty: '',
  bountyDays: 7,  // 默认7天
  content: '',
  tags: []
})

// 监听分类变化，更新表单数据
watch(selectedCategory, (category) => {
  questionForm.value.category = category.id
})

// 标签相关
const newTag = ref('')

const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !questionForm.value.tags.includes(tag) && questionForm.value.tags.length < 5) {
    questionForm.value.tags.push(tag)
    newTag.value = ''
  }
}

const removeTag = (tag) => {
  questionForm.value.tags = questionForm.value.tags.filter(t => t !== tag)
}

// 提交问题
const submitQuestion = () => {
  // 表单验证
  if (!questionForm.value.title) {
    showToast('请输入问题标题', 'warning')
    return
  }
  if (!questionForm.value.category) {
    showToast('请选择问题分类', 'warning')
    return
  }
  if (!questionForm.value.content) {
    showToast('请输入问题描述', 'warning')
    return
  }

  // TODO: 调用接口提交问题
  console.log('提交问题:', questionForm.value)
  showToast('发布成功', 'success')
  router.push('/community/questions')
}

// 话题表单数据
const selectedTopicCategory = ref(categories[0])
const newTopicTag = ref('')
const topicForm = ref({
  title: '',
  category: '',
  optionA: '',
  optionB: '',
  content: '',
  tags: []
})

// 监听话题分类变化
watch(selectedTopicCategory, (category) => {
  topicForm.value.category = category.id
})

// 话题标签相关
const addTopicTag = () => {
  const tag = newTopicTag.value.trim()
  if (tag && !topicForm.value.tags.includes(tag) && topicForm.value.tags.length < 5) {
    topicForm.value.tags.push(tag)
    newTopicTag.value = ''
  }
}

const removeTopicTag = (tag) => {
  topicForm.value.tags = topicForm.value.tags.filter(t => t !== tag)
}

// 提交话题
const submitTopic = () => {
  // 表单验证
  if (!topicForm.value.title) {
    showToast('请输入话题主题', 'warning')
    return
  }
  if (!topicForm.value.category) {
    showToast('请选择话题分类', 'warning')
    return
  }
  if (!topicForm.value.optionA || !topicForm.value.optionB) {
    showToast('请填写投票选项', 'warning')
    return
  }
  if (!topicForm.value.content) {
    showToast('请输入话题描述', 'warning')
    return
  }

  // TODO: 调用接口提交话题
  console.log('提交话题:', topicForm.value)
  showToast('发布成功', 'success')
  router.push('/community/topics')
}

// 自动保存相关
let autoSaveTimer = null
const AUTOSAVE_INTERVAL = 30000 // 30秒
const DRAFT_KEY_PREFIX = 'content_draft_'

// 保存草稿
const saveDraft = () => {
  const formData = {
    type: selectedType.value,
    data: selectedType.value === 'article' ? articleForm.value :
          selectedType.value === 'topic' ? topicForm.value :
          questionForm.value
  }
  localStorage.setItem(DRAFT_KEY_PREFIX + selectedType.value, JSON.stringify(formData))
  showToast('已自动保存草稿', 'info')
}

// 加载草稿
const loadDraft = () => {
  const draft = localStorage.getItem(DRAFT_KEY_PREFIX + selectedType.value)
  if (draft) {
    try {
      const { type, data } = JSON.parse(draft)
      if (type === selectedType.value) {
        if (type === 'article') articleForm.value = { ...data }
        else if (type === 'topic') topicForm.value = { ...data }
        else if (type === 'question') questionForm.value = { ...data }
        showToast('已恢复上次编辑的内容', 'info')
      }
    } catch (error) {
      console.error('加载草稿失败:', error)
    }
  }
}

// 清除草稿
const clearDraft = () => {
  localStorage.removeItem(DRAFT_KEY_PREFIX + selectedType.value)
}

// 开始自动保存
const startAutoSave = () => {
  stopAutoSave() // 先清除可能存在的定时器
  autoSaveTimer = setInterval(saveDraft, AUTOSAVE_INTERVAL)
}

// 停止自动保存
const stopAutoSave = () => {
  if (autoSaveTimer) {
    clearInterval(autoSaveTimer)
    autoSaveTimer = null
  }
}

// 监听类型变化
watch(selectedType, (newType) => {
  stopAutoSave()
  loadDraft()
  startAutoSave()
})

// 组件挂载时
onMounted(() => {
  loadDraft()
  startAutoSave()
})

// 组件卸载前
onBeforeUnmount(() => {
  stopAutoSave()
  saveDraft() // 最后保存一次
})

// 提交文章
const submitArticle = async () => {
  // 表单验证
  if (!articleForm.value.title) {
    showToast('请输入文章标题', 'warning')
    return
  }
  if (!articleForm.value.category) {
    showToast('请选择文章分类', 'warning')
    return
  }
  if (!articleForm.value.content) {
    showToast('请输入文章内容', 'warning')
    return
  }

  try {
    // TODO: 调用接口提交文章
    console.log('提交文章:', articleForm.value)
    clearDraft() // 提交成功后清除草稿
    showToast('发布成功', 'success')
    router.push('/community/articles')
  } catch (error) {
    console.error('提交文章失败:', error)
    showToast('发布失败，请稍后重试', 'error')
  }
}
</script> 