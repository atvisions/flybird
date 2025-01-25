<template>
  <div class="icon-element" :style="elementStyle">
    <component 
      :is="iconComponent" 
      v-bind="iconProps"
      :style="{
        width: '100%',
        height: '100%',
        color: props.fill,
        stroke: props.stroke,
        strokeWidth: `${props.strokeWidth}px`,
        opacity: props.opacity,
        filter: `drop-shadow(${props.shadowOffsetX}px ${props.shadowOffsetY}px ${props.shadowBlur}px ${props.shadowColor})`
      }"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import * as IconPark from '@icon-park/vue-next'
import * as AntdIcons from '@ant-design/icons-vue'
import * as Ionicons from '@vicons/ionicons5'
import * as Carbon from '@vicons/carbon'
import * as Tabler from '@vicons/tabler'
import { Icon } from '@iconify/vue'

const props = defineProps({
  width: {
    type: Number,
    default: 24
  },
  height: {
    type: Number,
    default: 24
  },
  iconType: {
    type: String,
    required: true
  },
  component: {
    type: String,
    required: true
  },
  theme: {
    type: String,
    default: null
  },
  icon: {
    type: String,
    default: null
  },
  fill: {
    type: String,
    default: '#1890ff'
  },
  stroke: {
    type: String,
    default: '#096dd9'
  },
  strokeWidth: {
    type: Number,
    default: 2
  },
  opacity: {
    type: Number,
    default: 1
  },
  shadowColor: {
    type: String,
    default: 'rgba(0, 0, 0, 0.3)'
  },
  shadowOffsetX: {
    type: Number,
    default: 0
  },
  shadowOffsetY: {
    type: Number,
    default: 0
  },
  shadowBlur: {
    type: Number,
    default: 0
  },
  rotate: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update'])

// 根据组件名称获取实际组件
const iconComponent = computed(() => {
  if (props.icon) {
    return Icon
  }
  
  // 从不同的图标库中查找组件
  const libraries = {
    ...IconPark,
    ...AntdIcons,
    ...Ionicons,
    ...Carbon,
    ...Tabler
  }
  
  return libraries[props.component] || null
})

// 构建图标属性
const iconProps = computed(() => {
  const baseProps = {}

  if (props.icon) {
    return {
      ...baseProps,
      icon: props.icon
    }
  }

  if (props.theme) {
    return {
      ...baseProps,
      theme: props.theme
    }
  }

  return baseProps
})

// 元素样式
const elementStyle = computed(() => ({
  width: `${props.width}px`,
  height: `${props.height}px`,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  transform: `rotate(${props.rotate}deg)`,
  transformOrigin: 'center'
}))

// 处理属性更新
const handleUpdate = (key, value) => {
  emit('update', {
    props: {
      [key]: value
    }
  })
}
</script>

<style scoped>
.icon-element {
  position: relative;
}

.icon-element :deep(svg) {
  width: 100%;
  height: 100%;
  transition: all 0.3s ease;
}
</style> 