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

      <!-- 简历组件面板 -->
      <div v-else-if="activeTab === 'resume'" class="resume-panel">
        <div v-for="component in resumeComponents" :key="component.key" class="resume-category">
          <div class="resume-component-item"
            draggable="true"
            @dragstart="handleDragStart($event, component)"
          >
            <div class="component-icon">
              <component :is="getResumeComponentIcon(component.key)" />
            </div>
            <div class="component-info">
              <div class="component-name">{{ component.label }}</div>
              <div class="component-desc">{{ getComponentDescription(component) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useTabs } from '../composables/useTabs'
import { useComponents } from '../composables/useComponents'
import * as Icons from '@icon-park/vue-next'
import IconPanel from './icons/IconPanel.vue'
import { resumeComponents } from '../config/resume-components'

const { activeTab, tabs, switchTab } = useTabs()
const { components } = useComponents()

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

// 统一的拖拽处理函数
const handleDragStart = (event, item) => {
  let dragData = null
  
  if (item.type === 'icon') {
    dragData = {
      type: 'icon',
      ...item
    }
  } else if (item.type === 'component') {
    dragData = {
      type: 'component',
      ...item
    }
  } else if (item.type === 'group') {
    // 处理简历组件组
    dragData = {
      type: 'resume-group',
      key: item.key,
      label: item.label,
      dataKey: item.dataKey,
      fields: item.fields,
      isArray: item.isArray || false,
      props: {
        ...item.props,
        background: '#fff',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)'
      }
    }
  }

  if (dragData) {
    event.dataTransfer.setData('application/json', JSON.stringify(dragData))
  }
}

const getFieldIcon = (type) => {
  const iconMap = {
    text: Icons.Text,
    richText: Icons.Editor,
    name: Icons.User,
    phone: Icons.Phone,
    email: Icons.Mail,
    location: Icons.Location,
    personal_summary: Icons.Notes,
    company: Icons.Building,
    position: Icons.IdCard,
    duration: Icons.Time,
    description: Icons.Editor,
    school: Icons.School,
    major: Icons.Book,
    degree: Icons.Certificate,
    skills: Icons.Star,
    level: Icons.Level
  }
  return iconMap[type] || Icons.Help
}

// 获取简历组件图标
const getResumeComponentIcon = (key) => {
  const iconMap = {
    basicInfo: Icons.User,
    jobIntention: Icons.Target,
    education: Icons.School,
    workExperience: Icons.Building,
    skills: Icons.Star,
    languages: Icons.Language,
    certificates: Icons.Certificate,
    projects: Icons.Folder,
    portfolio: Icons.Gallery
  }
  return iconMap[key] || Icons.Help
}

// 获取组件描述
const getComponentDescription = (component) => {
  const descriptions = {
    basicInfo: '姓名、头像、联系方式等基本信息',
    jobIntention: '期望职位、薪资、城市等求职意向',
    education: '学历、专业、学校等教育经历',
    workExperience: '公司、职位、工作内容等经历',
    skills: '专业技能及熟练程度',
    languages: '语言能力水平',
    certificates: '获得的证书和奖项',
    projects: '参与的项目经历',
    portfolio: '作品集展示'
  }
  return descriptions[component.key] || '简历组件'
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

.resume-panel {
  padding: 4px 8px;
}

.resume-category {
  margin-bottom: 12px;
}

.resume-category:last-child {
  margin-bottom: 0;
}

.resume-component-item {
  height: 72px;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.04);
  border-radius: 12px;
  display: flex;
  align-items: center;
  padding: 16px;
  cursor: move;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
  position: relative;
  overflow: hidden;
}

.resume-component-item::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 0%, rgba(24, 144, 255, 0.02) 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.resume-component-item:hover {
  border-color: rgba(24, 144, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 
    0 8px 24px rgba(24, 144, 255, 0.06),
    0 2px 8px rgba(24, 144, 255, 0.04);
}

.resume-component-item:hover::after {
  opacity: 1;
}

.component-icon {
  width: 40px;
  height: 40px;
  font-size: 20px;
  color: #1890ff;
  background: rgba(24, 144, 255, 0.04);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  transition: all 0.3s;
}

.resume-component-item:hover .component-icon {
  transform: scale(1.05);
  background: rgba(24, 144, 255, 0.08);
}

.component-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.component-name {
  font-size: 14px;
  color: #333;
  font-weight: 600;
}

.component-desc {
  font-size: 12px;
  color: #999;
  line-height: 1.5;
}
</style> 