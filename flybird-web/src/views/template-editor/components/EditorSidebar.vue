<template>
  <div class="editor-sidebar">
    <div class="sidebar-tabs">
      <div 
        v-for="tab in tabs" 
        :key="tab.key"
        class="tab-item"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        <component :is="tab.icon" theme="outline" size="20" />
        <span>{{ tab.label }}</span>
      </div>
    </div>

    <!-- 模板列表 -->
    <div v-if="activeTab === 'templates'" class="tab-content">
      <h3>模板</h3>
      <!-- TODO: 添加模板列表 -->
    </div>

    <!-- 组件列表 -->
    <div v-if="activeTab === 'components'" class="tab-content">
      <div 
        v-for="group in componentGroups" 
        :key="group.title"
        class="component-section"
      >
        <div class="component-group">
          <div
            v-for="component in group.items"
            :key="`${component.type}-${component.subType}`"
            class="component-item"
            draggable="true"
            @dragstart="handleDragStart($event, component)"
          >
            <component :is="component.icon" theme="outline" size="24" />
            <span>{{ component.label }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 图标列表 -->
    <div v-if="activeTab === 'icons'" class="tab-content">
      <h3>图标</h3>
      <!-- TODO: 添加图标列表 -->
    </div>
  </div>
</template>

<script setup>
import { useTabs } from '../composables/useTabs'
import { useComponents } from '../composables/useComponents'

const { tabs, activeTab } = useTabs()
const { componentGroups, handleDragStart } = useComponents()
</script>

<style scoped>
@import '../styles/sidebar.css';
</style> 