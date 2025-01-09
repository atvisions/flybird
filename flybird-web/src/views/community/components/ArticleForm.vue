<template>
  <div class="space-y-6 p-4 lg:p-6 pb-24">
    <!-- 标题 -->
    <div>
      <input
        type="text"
        v-model="form.title"
        class="block w-full text-xl font-medium border-0 focus:ring-0 p-0"
        placeholder="输入文章标题..."
      >
    </div>

    <!-- 分类 -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">文章分类</label>
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

    <!-- 缩略图 -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">文章封面</label>
      <div class="flex items-center gap-4">
        <div 
          class="relative w-48 h-32 rounded-lg border-2 border-dashed border-gray-300 hover:border-violet-500 transition-colors overflow-hidden group"
          :class="{ 'border-solid border-violet-500': form.cover }"
        >
          <input
            type="file"
            accept="image/*"
            class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
            @change="handleCoverChange"
          >
          <div v-if="!form.cover" class="absolute inset-0 flex flex-col items-center justify-center text-gray-400 group-hover:text-violet-500">
            <PhotoIcon class="w-8 h-8 mb-1" />
            <span class="text-xs">点击上传封面</span>
          </div>
          <img 
            v-else 
            :src="form.cover" 
            class="w-full h-full object-cover"
            alt=""
          >
          <button 
            v-if="form.cover"
            type="button"
            class="absolute top-2 right-2 p-1 bg-black/50 rounded-full text-white opacity-0 group-hover:opacity-100 transition-opacity"
            @click.stop="removeCover"
          >
            <XMarkIcon class="w-4 h-4" />
          </button>
        </div>
        <div class="flex-1 text-sm text-gray-500">
          <p>建议尺寸：1200x675 像素</p>
          <p>支持 jpg、png 格式，最大 2MB</p>
        </div>
      </div>
    </div>

    <!-- 文章摘要 -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">文章摘要</label>
      <textarea
        v-model="form.summary"
        rows="3"
        class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
        placeholder="写一段简短的介绍，会显示在文章列表中"
      ></textarea>
    </div>

    <!-- 编辑器 -->
    <div>
      <Toolbar
        style="border-bottom: 1px solid #ccc"
        :editor="editorRef"
        :defaultConfig="toolbarConfig"
        mode="default"
      />
      <Editor
        v-model="form.content"
        style="height: 500px; overflow-y: hidden;"
        :defaultConfig="editorConfig"
        mode="default"
        @onCreated="handleCreated"
        @onChange="handleChange"
      />
    </div>
  </div>

  <!-- 底部按钮 -->
  <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-4 z-50">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500">{{ lastSaveTime ? `上次保存: ${formatTime(lastSaveTime)}` : '文章将自动保存' }}</span>
        <div class="flex items-center gap-4">
          <button 
            class="px-6 h-10 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors"
            @click="$router.back()"
          >
            取消
          </button>
          <button 
            class="px-6 h-10 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
            @click="handleSubmit"
          >
            发布文章
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { formatTime } from '@/utils/time'
import { showToast } from '@/components/ToastMessage'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { 
  ChevronUpDownIcon, 
  CheckIcon,
  CodeBracketIcon,
  ServerIcon,
  DevicePhoneMobileIcon,
  ChartBarIcon,
  DatabaseIcon,
  CpuChipIcon,
  BeakerIcon,
  PhotoIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

// 编辑器实例
const editorRef = ref(null)

// 编辑器内容
const editorContent = ref('')

// 编辑器配置
const editorConfig = {
  placeholder: '开始写作...',
  MENU_CONF: {
    // 代码块配置
    codeBlock: {
      languages: [
        { title: 'Plain Text', value: 'text' },
        { title: 'HTML', value: 'html' },
        { title: 'CSS', value: 'css' },
        { title: 'JavaScript', value: 'javascript' },
        { title: 'TypeScript', value: 'typescript' },
        { title: 'Vue', value: 'vue' },
        { title: 'Python', value: 'python' },
        { title: 'Java', value: 'java' },
        { title: 'Go', value: 'go' },
        { title: 'Shell', value: 'shell' },
        { title: 'SQL', value: 'sql' },
        { title: 'JSON', value: 'json' }
      ],
      // 代码高亮配置
      highlightConfig: {
        // 使用 highlight.js
        hljs: {
          lineNumbers: true, // 显示行号
          wrap: true // 超出换行
        }
      }
    }
  }
}

// 工具栏配置
const toolbarConfig = {
  excludeKeys: [
    'group-video',
    'insertTable',
    'fullScreen'
  ]
}

// 表单数据
const form = ref({
  title: '',
  category: '',
  content: '',
  tags: [],
  cover: '',
  summary: '',
  isPublic: true,
  allowComment: true
})

// 最后保存时间
const lastSaveTime = ref(null)

// 自动保存相关
let autoSaveTimer = null
const AUTOSAVE_INTERVAL = 30000 // 30秒
const DRAFT_KEY = 'article_draft'

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

// 监听分类变化
watch(selectedCategory, (category) => {
  form.value.category = category.id
})

// 处理封面图片上传
const handleCoverChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    showToast('请选择图片文件', 'error')
    return
  }

  // 验证文件大小（2MB）
  if (file.size > 2 * 1024 * 1024) {
    showToast('图片大小不能超过 2MB', 'error')
    return
  }

  // 读取文件预览
  const reader = new FileReader()
  reader.onload = (e) => {
    form.value.cover = e.target.result
  }
  reader.readAsDataURL(file)
}

// 移除封面图片
const removeCover = () => {
  form.value.cover = ''
}

// 保存草稿
const saveDraft = () => {
  // 保存当前编辑器内容
  if (editorRef.value) {
    editorContent.value = editorRef.value.getHtml()
  }
  
  // 保存所有表单数据和编辑器内容
  const draftData = {
    ...form.value,
    editorContent: editorContent.value,
    selectedCategory: selectedCategory.value
  }
  
  localStorage.setItem(DRAFT_KEY, JSON.stringify(draftData))
  lastSaveTime.value = new Date()
}

// 加载草稿
const loadDraft = () => {
  const draft = localStorage.getItem(DRAFT_KEY)
  if (draft) {
    try {
      const draftData = JSON.parse(draft)
      
      // 保存编辑器内容
      editorContent.value = draftData.editorContent || ''
      
      // 先设置编辑器内容
      if (editorRef.value && editorContent.value) {
        editorRef.value.setHtml(editorContent.value)
      }
      
      // 恢复表单数据
      form.value = {
        title: draftData.title || '',
        category: draftData.category || '',
        content: editorContent.value,
        tags: draftData.tags || [],
        cover: draftData.cover || '',
        summary: draftData.summary || '',
        isPublic: draftData.isPublic ?? true,
        allowComment: draftData.allowComment ?? true
      }

      // 恢复选中的分类
      if (draftData.selectedCategory) {
        selectedCategory.value = draftData.selectedCategory
      }

      lastSaveTime.value = new Date()
      showToast('已恢复上次编辑的内容', 'info')
    } catch (error) {
      console.error('加载草稿失败:', error)
    }
  }
}

// 清除草稿
const clearDraft = () => {
  localStorage.removeItem(DRAFT_KEY)
}

// 开始自动保存
const startAutoSave = () => {
  stopAutoSave()
  autoSaveTimer = setInterval(saveDraft, AUTOSAVE_INTERVAL)
}

// 停止自动保存
const stopAutoSave = () => {
  if (autoSaveTimer) {
    clearInterval(autoSaveTimer)
    autoSaveTimer = null
  }
}

// 编辑器创建完成
const handleCreated = (editor) => {
  editorRef.value = editor
  // 编辑器创建完成后加载草稿
  loadDraft()
}

// 编辑器内容变化
const handleChange = () => {
  if (editorRef.value) {
    const html = editorRef.value.getHtml()
    editorContent.value = html
    form.value.content = html
    saveDraft() // 内容变化时保存草稿
  }
  emit('update:modelValue', form.value)
}

// 提交表单
const handleSubmit = () => {
  // 表单验证
  if (!form.value.title) {
    showToast('请输入文章标题', 'warning')
    return
  }
  if (!form.value.category) {
    showToast('请选择文章分类', 'warning')
    return
  }
  if (!form.value.content) {
    showToast('请输入文章内容', 'warning')
    return
  }

  emit('submit', form.value)
}

// 监听父组件数据变化
watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal && Object.keys(newVal).length > 0) {
      form.value = { ...newVal }
    }
  },
  { deep: true }
)

onMounted(() => {
  startAutoSave()
})

onBeforeUnmount(() => {
  stopAutoSave()
  saveDraft() // 最后保存一次
  if (editorRef.value) {
    editorRef.value.destroy()
  }
})
</script>

<style src="@wangeditor/editor/dist/css/style.css"></style> 