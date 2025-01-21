<template>
  <div class="editor-sidebar">
    <div class="sidebar-header">
      <div class="tab-container">
        <div 
          v-for="tab in tabs" 
          :key="tab.key"
          class="tab-item"
          :class="{ active: activeTab === tab.key }"
          @click="switchTab(tab.key)"
        >
          <span class="tab-text">{{ tab.label }}</span>
          <div class="tab-background" v-if="activeTab === tab.key"></div>
        </div>
      </div>
    </div>

    <div class="sidebar-content">
      <template v-if="activeTab === 'components'">
        <div 
          v-for="group in components" 
          :key="group.type"
          class="component-group"
        >
          <div class="group-title">{{ group.title }}</div>
          <div class="group-content">
            <div 
              v-for="item in group.items" 
              :key="item.type"
              class="component-item"
              draggable="true"
              @dragstart="handleDragStart($event, item)"
            >
              <div class="item-icon">
                <component :is="getIconComponent(item.icon)" />
              </div>
              <div class="item-name">{{ item.name }}</div>
            </div>
          </div>
        </div>
      </template>

      <template v-else-if="activeTab === 'layers'">
        <div class="layers-panel">
          <!-- TODO: 实现图层面板 -->
          图层面板开发中...
        </div>
      </template>

      <template v-else-if="activeTab === 'icons'">
        <IconPanel @select-icon="handleIconSelect" />
      </template>

      <template v-else-if="activeTab === 'templates'">
        <div class="templates-panel">
          <!-- TODO: 实现模板面板 -->
          模板面板开发中...
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTabs } from '../composables/useTabs'
import { useComponents } from '../composables/useComponents'
import * as Icons from '@icon-park/vue-next'
import IconPanel from './icons/IconPanel.vue'

const { activeTab, tabs, switchTab } = useTabs()
const { components, handleDragStart } = useComponents()

// 获取图标组件
const getIconComponent = (iconName) => {
  const componentName = iconName
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join('')
  return Icons[componentName] || Icons.Help
}

const handleIconSelect = (iconData) => {
  handleDragStart(new CustomEvent('dragstart'), iconData)
}
</script>

<style scoped>
.editor-sidebar {
  width: 260px;
  height: 100%;
  background: #fff;
  display: flex;
  flex-direction: column;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.08),
    0 0 0 1px rgba(0, 0, 0, 0.04);
}

.sidebar-header {
  padding: 16px;
  background: linear-gradient(to bottom, #fff, rgba(255, 255, 255, 0.95));
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.02);
}

.tab-container {
  position: relative;
  display: flex;
  background: rgba(28, 31, 35, 0.06);
  border-radius: 12px;
  padding: 4px;
  gap: 4px;
}

.tab-item {
  position: relative;
  flex: 1;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 8px;
  overflow: hidden;
  user-select: none;
}

.tab-text {
  position: relative;
  z-index: 2;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-background {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #fff 0%, rgba(255, 255, 255, 0.95) 100%);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 0 0 1px rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  z-index: 1;
  animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-item:hover .tab-text {
  color: #1890ff;
}

.tab-item.active .tab-text {
  color: #1890ff;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.95), #fff);
}

.sidebar-content::-webkit-scrollbar {
  width: 4px;
}

.sidebar-content::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 2px;
}

.component-group {
  margin-bottom: 24px;
}

.group-title {
  font-size: 13px;
  color: #999;
  margin-bottom: 12px;
  padding-left: 4px;
}

.group-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.component-item {
  height: 80px;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.04);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: move;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}

.component-item:hover {
  border-color: rgba(24, 144, 255, 0.2);
  transform: translateY(-1px);
  box-shadow: 
    0 4px 16px rgba(24, 144, 255, 0.1),
    0 1px 4px rgba(24, 144, 255, 0.05);
}

.component-item:active {
  transform: translateY(0);
}

.item-icon {
  font-size: 24px;
  color: #666;
  margin-bottom: 8px;
  transition: all 0.3s;
}

.component-item:hover .item-icon {
  color: #1890ff;
  transform: scale(1.1);
}

.item-name {
  font-size: 12px;
  color: #666;
  transition: color 0.3s;
}

.component-item:hover .item-name {
  color: #1890ff;
}

.layers-panel,
.templates-panel {
  color: #999;
  text-align: center;
  padding: 40px 0;
}
</style> 