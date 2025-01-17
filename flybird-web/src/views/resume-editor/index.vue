<template>
  <div class="resume-editor">
    <!-- 顶部工具栏 -->
    <div class="editor-toolbar">
      <div class="toolbar-left">
        <v-btn
          icon="mdi-arrow-left"
          variant="text"
          density="comfortable"
          @click="handleExit"
        ></v-btn>
        <div class="resume-name" @click="startEditName">
          <span v-if="!isEditingName">{{ resumeName }}</span>
          <v-text-field
            v-else
            v-model="editingName"
            density="compact"
            variant="underlined"
            hide-details
            autofocus
            @blur="finishEditName"
            @keyup.enter="finishEditName"
          ></v-text-field>
        </div>
      </div>
      <div class="toolbar-center">
        <v-btn
          icon="mdi-undo"
          variant="text"
          density="comfortable"
          :disabled="!canUndo"
          @click="handleUndo"
          :title="'撤销'"
        ></v-btn>
        <v-btn
          icon="mdi-redo"
          variant="text"
          density="comfortable"
          :disabled="!canRedo"
          @click="handleRedo"
          :title="'重做'"
        ></v-btn>
      </div>
      <div class="toolbar-right">
        <v-btn
          color="primary"
          prepend-icon="mdi-content-save"
          @click="showSaveDialog = true"
        >
          保存模板
        </v-btn>
        
        <v-btn
          color="info"
          prepend-icon="mdi-eye"
          class="ml-2"
          @click="previewTemplate"
        >
          预览
        </v-btn>
      </div>
    </div>

    <div class="editor-content">
      <!-- 左侧工具面板 -->
      <ToolbarPanel
        ref="toolbarRef"
        @element-dragstart="handleElementDragStart"
        @template-select="handleTemplateSelect"
        @preview-image="handlePreviewImage"
      />

      <!-- 中间画布区域 -->
      <Canvas
        ref="canvas"
        :scale="scale"
        @element-select="handleElementSelect"
        @data-fields-update="handleDataFieldsUpdate"
      />

      <!-- 右侧属性面板 -->
      <PropertyPanel
        :selected-element="selectedElement"
        :data-fields="dataFields"
        @update="handleElementUpdate"
      />
    </div>

    <!-- 底部工具栏 -->
    <div class="editor-footer">
      <div class="zoom-controls">
        <v-btn
          icon="mdi-minus"
          variant="text"
          density="comfortable"
          @click="decreaseScale"
          :disabled="scale <= 0.25"
        ></v-btn>
        <div class="zoom-slider">
          <v-slider
            v-model="scalePercentage"
            :min="25"
            :max="200"
            :step="5"
            hide-details
            density="compact"
            color="primary"
            track-color="grey-lighten-2"
          >
            <template v-slot:append>
              <div class="zoom-text">{{ Math.round(scalePercentage) }}%</div>
            </template>
          </v-slider>
        </div>
        <v-btn
          icon="mdi-plus"
          variant="text"
          density="comfortable"
          @click="increaseScale"
          :disabled="scale >= 2"
        ></v-btn>
      </div>
      <div class="footer-right">
        <v-btn
          :icon="isFullscreen ? 'mdi-fullscreen-exit' : 'mdi-fullscreen'"
          variant="text"
          density="comfortable"
          @click="toggleFullscreen"
          :title="isFullscreen ? '退出全屏' : '全屏显示'"
        ></v-btn>
      </div>
    </div>

    <!-- 保存模板对话框 -->
    <SaveTemplateDialog
      v-model="showSaveDialog"
      @save="handleSaveTemplate"
    />

    <!-- 消息提示 -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
    >
      {{ snackbar.text }}
    </v-snackbar>

    <!-- 图片预览对话框 -->
    <v-dialog v-model="previewDialog.show" width="500">
      <v-card class="preview-dialog">
        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          class="close-btn"
          @click="previewDialog.show = false"
        ></v-btn>
        <v-card-text class="pa-0">
          <div class="preview-container">
            <img :src="previewDialog.imageUrl" alt="预览图片" class="preview-image">
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ToolbarPanel from './components/ToolbarPanel.vue'
import Canvas from './components/Canvas.vue'
import PropertyPanel from './components/PropertyPanel.vue'
import SaveTemplateDialog from './components/SaveTemplateDialog.vue'
import { useTemplateStore } from '@/stores/template'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account'

const canvas = ref(null)
const toolbarRef = ref(null)
const selectedElement = ref(null)
const dataFields = ref([])
const showSaveDialog = ref(false)
const scale = ref(1)
const isFullscreen = ref(false)

// 计算缩放百分比
const scalePercentage = computed({
  get: () => scale.value * 100,
  set: (value) => {
    scale.value = value / 100
  }
})

// 增加缩放
const increaseScale = () => {
  if (scale.value < 2) {
    scale.value = Math.min(2, scale.value + 0.1)
  }
}

// 减少缩放
const decreaseScale = () => {
  if (scale.value > 0.25) {
    scale.value = Math.max(0.25, scale.value - 0.1)
  }
}

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const templateStore = useTemplateStore()
const router = useRouter()
const accountStore = useAccountStore()

// 简历名称相关
const isEditingName = ref(false)
const editingName = ref('')
const resumeName = ref('')

// 初始化简历名称
const initResumeName = () => {
  const userInfo = accountStore.userInfo
  resumeName.value = userInfo?.nickname ? `${userInfo.nickname}的简历` : '我的简历'
}

// 开始编辑名称
const startEditName = () => {
  editingName.value = resumeName.value
  isEditingName.value = true
}

// 完成编辑名称
const finishEditName = () => {
  if (editingName.value.trim()) {
    resumeName.value = editingName.value.trim()
  }
  isEditingName.value = false
}

// 退出编辑器
const handleExit = () => {
  router.push('/resume/list')
}

// 显示消息
const showMessage = (text, color = 'success') => {
  snackbar.value = {
    show: true,
    text,
    color
  }
}

// 处理元素选择
const handleElementSelect = (element) => {
  selectedElement.value = element
}

// 处理数据字段更新
const handleDataFieldsUpdate = (fields) => {
  dataFields.value = fields
}

// 处理元素更新
const handleElementUpdate = (update) => {
  if (canvas.value) {
    canvas.value.handleElementUpdate(update)
  }
}

// 预览模板
const previewTemplate = () => {
  // TODO: 实现预览功能
  showMessage('预览功能开发中')
}

// 处理保存模板
const handleSaveTemplate = async (formData) => {
  try {
    const canvasData = canvas.value.getCanvasData()
    const templateData = {
      ...formData,
      content: {
        elements: canvasData.elements
      }
    }
    await templateStore.saveTemplate(templateData)
    showMessage('保存成功', 'success')
    showSaveDialog.value = false
    // 刷新模板列表
    toolbarRef.value.refreshTemplates()
  } catch (error) {
    showMessage(error.message || '保存失败', 'error')
  }
}

// 处理模板选择
const handleTemplateSelect = async (template) => {
  try {
    // 获取模板详情
    const templateData = await templateStore.getTemplateDetail(template.id)
    console.log('模板详情:', templateData)
    
    // 加载模板内容到画布
    if (canvas.value && templateData.content) {
      await canvas.value.loadTemplate(templateData.content)
      showMessage('模板加载成功', 'success')
    } else {
      throw new Error('模板内容为空')
    }
  } catch (error) {
    console.error('加载模板失败:', error)
    showMessage(error.message || '加载模板失败', 'error')
  }
}

// 切换全屏
const toggleFullscreen = () => {
  if (!isFullscreen.value) {
    const canvasContainer = document.querySelector('.canvas-container')
    if (canvasContainer.requestFullscreen) {
      canvasContainer.requestFullscreen()
    } else if (canvasContainer.webkitRequestFullscreen) {
      canvasContainer.webkitRequestFullscreen()
    } else if (canvasContainer.msRequestFullscreen) {
      canvasContainer.msRequestFullscreen()
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen()
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen()
    }
  }
}

// 监听全屏变化
const handleFullscreenChange = () => {
  isFullscreen.value = !!document.fullscreenElement || 
                      !!document.webkitFullscreenElement || 
                      !!document.msFullscreenElement
}

// 撤销/重做状态
const canUndo = ref(false)
const canRedo = ref(false)

// 处理撤销
const handleUndo = () => {
  if (canvas.value) {
    canvas.value.undo()
  }
}

// 处理重做
const handleRedo = () => {
  if (canvas.value) {
    canvas.value.redo()
  }
}

// 更新撤销/重做状态
const updateUndoRedoState = (state) => {
  canUndo.value = state.canUndo
  canRedo.value = state.canRedo
}

// 图片预览对话框
const previewDialog = ref({
  show: false,
  imageUrl: ''
})

// 处理图片预览
const handlePreviewImage = (imageUrl) => {
  previewDialog.value = {
    show: true,
    imageUrl
  }
}

onMounted(() => {
  document.addEventListener('fullscreenchange', handleFullscreenChange)
  document.addEventListener('webkitfullscreenchange', handleFullscreenChange)
  document.addEventListener('msfullscreenchange', handleFullscreenChange)
  initResumeName()
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
  document.removeEventListener('webkitfullscreenchange', handleFullscreenChange)
  document.removeEventListener('msfullscreenchange', handleFullscreenChange)
})
</script>

<style scoped>
.resume-editor {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.editor-toolbar {
  height: 64px;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
}

.editor-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.editor-footer {
  height: 48px;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  background-color: #fff;
  border-top: 1px solid #e0e0e0;
}

.zoom-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px;
  border-radius: 4px;
  grid-column: 2;
  justify-self: center;
}

.footer-right {
  display: flex;
  align-items: center;
  grid-column: 3;
  justify-self: end;
}

.zoom-slider {
  width: 200px;
  margin: 0 8px;
}

.zoom-text {
  min-width: 48px;
  text-align: center;
  font-size: 14px;
  color: #606266;
}

/* 全屏时的样式 */
:fullscreen .canvas-container {
  background: #fff;
  width: 100vw;
  height: 100vh;
}

:-webkit-full-screen .canvas-container {
  background: #fff;
  width: 100vw;
  height: 100vh;
}

:-ms-fullscreen .canvas-container {
  background: #fff;
  width: 100vw;
  height: 100vh;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toolbar-right {
  display: flex;
  align-items: center;
}

.resume-name {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.resume-name:hover {
  background-color: #f5f5f5;
}

.resume-name :deep(.v-text-field) {
  width: 200px;
  font-size: 16px;
  font-weight: 500;
}

.toolbar-center {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-self: center;
}

.toolbar-right {
  justify-self: end;
}

.preview-dialog {
  position: relative;

  .close-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    z-index: 1;
    background: white;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

    &:hover {
      background: #f5f5f5;
    }
  }

  .preview-container {
    width: 500px;
    height: 707px; /* A4 比例：500 * 1.414 */
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .preview-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
}
</style> 