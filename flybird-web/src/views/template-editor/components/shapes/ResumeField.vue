<template>
  <div
    ref="fieldRef"
    class="resume-field canvas-element"
    :style="fieldStyle"
  >
    <template v-if="type === 'avatar'">
      <div class="avatar-field" :style="avatarStyle">
        <img 
          v-if="value" 
          :src="value" 
          :style="{ borderRadius: 'inherit' }"
          draggable="false"
        />
        <div 
          v-else 
          class="avatar-placeholder"
          :style="{ borderRadius: 'inherit' }"
          draggable="false"
        >
          <el-icon :size="40"><Avatar /></el-icon>
          <div class="avatar-text">头像</div>
        </div>
      </div>
    </template>
    <template v-else>
      <ResumeText
        :value="value"
        :label="label"
        :width="width"
        :height="height"
        :text-align="textAlign"
        :vertical-align="verticalAlign"
        :opacity="opacity"
        :color="color"
        :font-size="fontSize"
        :font-family="fontFamily"
        :font-weight="fontWeight"
        :font-style="fontStyle"
        :line-height="lineHeight"
        :data-path="dataPath"
      />
    </template>
    <div v-if="isSelected" class="resize-handles">
      <div class="resize-handle top-left" @mousedown.stop="startResize('top-left')"></div>
      <div class="resize-handle top-right" @mousedown.stop="startResize('top-right')"></div>
      <div class="resize-handle bottom-left" @mousedown.stop="startResize('bottom-left')"></div>
      <div class="resize-handle bottom-right" @mousedown.stop="startResize('bottom-right')"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ResumeAvatar from './ResumeAvatar.vue'
import ResumeText from './ResumeText.vue'
import ResumeTextarea from './ResumeTextarea.vue'
import { Avatar } from '@element-plus/icons-vue'

const props = defineProps({
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    required: true
  },
  value: {
    type: String,
    default: ''
  },
  dataPath: {
    type: String,
    default: ''
  },
  mappingType: {
    type: String,
    default: ''
  },
  width: {
    type: Number,
    required: true
  },
  height: {
    type: Number,
    required: true
  },
  textAlign: {
    type: String,
    default: 'left'
  },
  verticalAlign: {
    type: String,
    default: 'middle'
  },
  opacity: {
    type: Number,
    default: 1
  },
  fontSize: {
    type: Number,
    default: 14
  },
  fontFamily: {
    type: String,
    default: 'Arial'
  },
  fontWeight: {
    type: String,
    default: 'normal'
  },
  fontStyle: {
    type: String,
    default: 'normal'
  },
  color: {
    type: String,
    default: '#333333'
  },
  lineHeight: {
    type: Number,
    default: 1.5
  },
  borderRadius: {
    type: String,
    default: '0'
  },
  borderWidth: {
    type: Number,
    default: 0
  },
  borderStyle: {
    type: String,
    default: 'solid'
  },
  borderColor: {
    type: String,
    default: '#dcdfe6'
  },
  backgroundColor: {
    type: String,
    default: 'transparent'
  },
  isPreview: {
    type: Boolean,
    default: false
  },
  x: {
    type: Number,
    default: 0
  },
  y: {
    type: Number,
    default: 0
  },
  zIndex: {
    type: Number,
    default: 1
  },
  rotate: {
    type: Number,
    default: 0
  },
  isSelected: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:value'])

const fieldRef = ref(null)

const fieldStyle = computed(() => ({
  position: 'absolute',
  width: `${props.width}px`,
  height: `${props.height}px`,
  left: `${props.x}px`,
  top: `${props.y}px`,
  zIndex: props.zIndex,
  opacity: props.opacity,
  fontSize: `${props.fontSize}px`,
  fontWeight: props.fontWeight,
  color: props.color,
  lineHeight: props.lineHeight,
  borderRadius: props.borderRadius,
  transform: props.rotate ? `rotate(${props.rotate}deg)` : undefined
}))

const contentStyle = computed(() => ({
  fontSize: `${props.fontSize}px`,
  fontWeight: props.fontWeight,
  color: props.color,
  lineHeight: props.lineHeight
}))

const avatarStyle = computed(() => ({
  width: '100%',
  height: '100%',
  borderRadius: props.type === 'avatar' ? props.borderRadius || '50%' : props.borderRadius,
  border: props.borderWidth ? `${props.borderWidth}px ${props.borderStyle} ${props.borderColor}` : 'none',
  backgroundColor: props.backgroundColor,
  overflow: 'hidden',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center'
}))

const getFieldComponent = (type) => {
  const componentMap = {
    avatar: ResumeAvatar,
    text: ResumeText,
    textarea: ResumeTextarea
  }
  return componentMap[type] || ResumeText
}

const handleValueUpdate = (newValue) => {
  emit('update:value', newValue)
}

const startResize = (handle) => {
  // Implementation of startResize method
}

onUnmounted(() => {
  // Implementation of onUnmounted method
})
</script>

<style scoped>
.resume-field {
  position: absolute;
  user-select: none;
  box-sizing: border-box;
  min-width: 50px;
  min-height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: move;
}

.resume-field:hover {
  outline: 1px solid #409eff;
}

.resize-handles {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  pointer-events: none;
}

.resize-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #fff;
  border: 1px solid #409eff;
  pointer-events: auto;
  cursor: pointer;
  border-radius: 50%;
  z-index: 1;
}

.top-left {
  top: -4px;
  left: -4px;
  cursor: nw-resize;
}

.top-right {
  top: -4px;
  right: -4px;
  cursor: ne-resize;
}

.bottom-left {
  bottom: -4px;
  left: -4px;
  cursor: sw-resize;
}

.bottom-right {
  bottom: -4px;
  right: -4px;
  cursor: se-resize;
}

.avatar-field {
  width: 100% !important;
  height: 100% !important;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: #f5f7fa;
  box-sizing: border-box;
}

.avatar-field img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  color: #909399;
}

.avatar-text {
  margin-top: 8px;
  font-size: 14px;
}

.field-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 4px 8px;
  box-sizing: border-box;
}

.field-content:hover {
  color: #409eff;
}
</style> 