<template>
  <div class="space-y-6 pb-24 p-4 lg:p-6">
    <!-- 标题 -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">文章标题</label>
      <input
        type="text"
        v-model="articleForm.title"
        class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
        placeholder="请输入文章标题"
      >
    </div>

    <!-- 分类 -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">文章分类</label>
      <div class="relative">
        <!-- 分类选择 -->
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

    <!-- 封面图 -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">文章封面</label>
      <div class="flex items-center gap-4">
        <div 
          v-if="articleForm.cover"
          class="relative w-48 h-32 rounded-lg overflow-hidden group"
        >
          <img 
            :src="articleForm.cover" 
            class="w-full h-full object-cover"
          >
          <div 
            class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
          >
            <button 
              class="text-white text-sm"
              @click="articleForm.cover = ''"
            >
              删除封面
            </button>
          </div>
        </div>
        <div v-else>
          <button 
            class="w-48 h-32 rounded-lg border-2 border-dashed border-gray-300 hover:border-violet-500 transition-colors flex flex-col items-center justify-center gap-2"
            @click="uploadCover"
          >
            <PhotoIcon class="w-6 h-6 text-gray-400" />
            <span class="text-sm text-gray-500">点击上传封面</span>
          </button>
          <input
            ref="coverInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleCoverChange"
          >
        </div>
      </div>
    </div>

    <!-- 文章内容 -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">文章内容</label>
      <div class="border rounded-lg border-gray-300">
        <Toolbar
          :editor="editorRef"
          :defaultConfig="toolbarConfig"
          mode="default"
          style="border-bottom: 1px solid #e5e7eb"
        />
        <Editor
          v-model="articleForm.content"
          :defaultConfig="editorConfig"
          mode="default"
          @onCreated="handleCreated"
          style="height: 500px"
        />
      </div>
    </div>

    <!-- 标签 -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">添加标签</label>
      <div class="flex flex-wrap gap-2">
        <div
          v-for="tag in articleForm.tags"
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
          v-if="articleForm.tags.length < 5"
          type="text"
          v-model="newTag"
          @keydown.enter="addTag"
          class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
          placeholder="按回车添加标签"
        >
      </div>
      <p class="mt-1 text-xs text-gray-500">最多添加 5 个标签</p>
    </div>

    <!-- 发布按钮 -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-4 z-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center">
          <!-- 草稿状态提示 -->
          <span 
            v-if="lastSavedTime" 
            class="text-sm text-gray-500"
          >
            {{ lastSavedTime }} 已保存草稿
          </span>
          <div class="flex-1"></div>
          <button 
            class="px-6 h-10 border border-violet-600 text-violet-600 rounded-lg hover:bg-violet-50 transition-colors"
            @click="saveDraft"
          >
            保存草稿
          </button>
          <button 
            class="ml-4 px-6 h-10 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
            @click="submitArticle"
          >
            发布文章
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, shallowRef, onBeforeUnmount, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { 
  PhotoIcon, 
  XMarkIcon, 
  ChevronUpDownIcon, 
  CheckIcon,
  CodeBracketIcon,
  ServerIcon,
  DevicePhoneMobileIcon,
  ChartBarIcon,
  DatabaseIcon,
  CpuChipIcon,
  BeakerIcon
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'

// 引入编辑器样式
import '@wangeditor/editor/dist/css/style.css'

const router = useRouter()
const store = useStore()

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()

// 编辑器配置
const toolbarConfig = {
  excludeKeys: [
    'group-video',
    'insertTable',
    'group-indent',
    'headerSelect'
  ]
}

const editorConfig = {
  placeholder: '请输入文章内容...',
  MENU_CONF: {
    uploadImage: {
      server: '/api/upload/image',
      fieldName: 'image',
      maxFileSize: 10 * 1024 * 1024, // 10M
      maxNumberOfFiles: 10,
      allowedFileTypes: ['image/*'],
      metaWithUrl: true,
      customInsert(res, insertFn) {
        // res 即服务端返回的数据
        insertFn(res.url, res.alt, res.href)
      },
    },
    codeSelectLang: {
      codeLangs: [
        { text: 'JavaScript', value: 'javascript' },
        { text: 'TypeScript', value: 'typescript' },
        { text: 'HTML', value: 'html' },
        { text: 'CSS', value: 'css' },
        { text: 'Vue', value: 'vue' },
        { text: 'Python', value: 'python' },
        { text: 'Java', value: 'java' },
        { text: 'Go', value: 'go' },
        { text: 'SQL', value: 'sql' },
        { text: 'Shell', value: 'shell' }
      ]
    }
  }
}

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})

const handleCreated = (editor) => {
  editorRef.value = editor
}

// 文章表单数据
const articleForm = ref({
  title: '',
  category: '',
  cover: '',
  content: '',
  tags: []
})

// 标签相关
const newTag = ref('')

const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !articleForm.value.tags.includes(tag) && articleForm.value.tags.length < 5) {
    articleForm.value.tags.push(tag)
    newTag.value = ''
  }
}

const removeTag = (tag) => {
  articleForm.value.tags = articleForm.value.tags.filter(t => t !== tag)
}

// 封面图上传
const coverInput = ref(null)

const uploadCover = () => {
  coverInput.value.click()
}

const handleCoverChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  // TODO: 调用上传接口
  const reader = new FileReader()
  reader.onload = (e) => {
    articleForm.value.cover = e.target.result
  }
  reader.readAsDataURL(file)
}

// 草稿相关
const DRAFT_KEY = 'article_draft'
const lastSavedTime = ref('')
const autoSaveTimer = ref(null)

// 格式化时间
const formatTime = (date) => {
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) { // 小于1分钟
    return '刚刚'
  } else if (diff < 3600000) { // 小于1小时
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) { // 小于24小时
    return `${Math.floor(diff / 3600000)}小时前`
  } else {
    return date.toLocaleString()
  }
}

// 保存草稿
const saveDraft = () => {
  const draft = {
    ...articleForm.value,
    savedAt: new Date().toISOString()
  }
  localStorage.setItem(DRAFT_KEY, JSON.stringify(draft))
  lastSavedTime.value = formatTime(new Date())
  showToast('草稿已保存', 'success')
  // 跳转到用户中心的草稿箱
  router.push({
    path: '/user',
    query: { 
      tab: 'home',
      currentTab: 'drafts'
    }
  })
}

// 加载草稿
const loadDraft = () => {
  const draft = localStorage.getItem(DRAFT_KEY)
  if (draft) {
    const data = JSON.parse(draft)
    articleForm.value = {
      title: data.title || '',
      category: data.category || '',
      cover: data.cover || '',
      content: data.content || '',
      tags: data.tags || []
    }
    if (data.category) {
      selectedCategory.value = categories.find(c => c.id === data.category) || categories[0]
    }
    lastSavedTime.value = formatTime(new Date(data.savedAt))
  }
}

// 自动保存
const startAutoSave = () => {
  autoSaveTimer.value = setInterval(() => {
    if (articleForm.value.title || articleForm.value.content) {
      saveDraft()
    }
  }, 60000) // 每分钟自动保存
}

// 清除草稿
const clearDraft = () => {
  localStorage.removeItem(DRAFT_KEY)
  lastSavedTime.value = ''
}

// 组件挂载时加载草稿并开启自动保存
onMounted(() => {
  loadDraft()
  startAutoSave()
})

// 组件销毁时清除定时器
onBeforeUnmount(() => {
  if (autoSaveTimer.value) {
    clearInterval(autoSaveTimer.value)
  }
})

// 提交文章
const submitArticle = () => {
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

  // TODO: 调用接口提交文章
  console.log('提交文章:', articleForm.value)
  clearDraft() // 发布成功后清除草稿
  showToast('发布成功', 'success')
  router.push({
    path: '/user',
    query: { 
      tab: 'home',
      currentTab: 'articles'
    }
  })
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

// 监听分类变化，更新表单数据
watch(selectedCategory, (category) => {
  articleForm.value.category = category.id
})
</script>

<style>
.w-e-bar {
  padding: 0 8px !important;
}
</style> 