<template>
  <div class="resume-editor">
    <!-- 顶部工具栏 -->
    <div class="editor-toolbar">
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

    <div class="editor-content">
      <!-- 左侧工具面板 -->
      <ToolbarPanel
        ref="toolbarRef"
        @element-dragstart="handleElementDragStart"
        @template-select="handleTemplateSelect"
      />

      <!-- 中间画布区域 -->
      <Canvas
        ref="canvas"
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ToolbarPanel from './components/ToolbarPanel.vue'
import Canvas from './components/Canvas.vue'
import PropertyPanel from './components/PropertyPanel.vue'
import SaveTemplateDialog from './components/SaveTemplateDialog.vue'
import { useTemplateStore } from '@/stores/template'

const canvas = ref(null)
const toolbarRef = ref(null)
const selectedElement = ref(null)
const dataFields = ref([])
const showSaveDialog = ref(false)
const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const templateStore = useTemplateStore()

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
</script>

<style scoped>
.resume-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f5f5f5;
}

.editor-toolbar {
  padding: 8px 16px;
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
}

.editor-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}
</style> 