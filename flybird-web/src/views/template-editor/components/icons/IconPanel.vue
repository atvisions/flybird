<template>
  <div class="icon-panel">
    <!-- 实心风格图标组 -->
    <div class="icon-group">
      <div class="icon-title">实心风格图标</div>
      <div class="icon-list">
        <div class="icon-item" 
          v-for="icon in filledIcons" 
          :key="icon.type" 
          @click="handleIconClick(icon)"
          :title="icon.label"
          draggable="true"
          @dragstart="handleDragStart($event, icon)"
          @dragend="handleDragEnd"
        >
          <svg-icon :component="icon.component" :size="20" />
        </div>
      </div>
    </div>

    <!-- 线框风格图标组 -->
    <div class="icon-group">
      <div class="icon-title">线框风格图标</div>
      <div class="icon-list">
        <div class="icon-item" 
          v-for="icon in outlineIcons" 
          :key="icon.type" 
          @click="handleIconClick(icon)"
          :title="icon.label"
          draggable="true"
          @dragstart="handleDragStart($event, icon)"
          @dragend="handleDragEnd"
        >
          <component :is="icon.component" :theme="themes.outline" :size="20" />
        </div>
      </div>
    </div>

    <!-- 多彩风格图标组 -->
    <div class="icon-group">
      <div class="icon-title">多彩风格图标</div>
      <div class="icon-list">
        <div class="icon-item" 
          v-for="icon in colorfulIcons" 
          :key="icon.type" 
          @click="handleIconClick(icon)"
          :title="icon.label"
          draggable="true"
          @dragstart="handleDragStart($event, icon)"
          @dragend="handleDragEnd"
        >
          <component :is="icon.component" :icon="icon.icon" width="20" height="20" />
        </div>
      </div>
    </div>

    <!-- 圆形风格图标组 -->
    <div class="icon-group">
      <div class="icon-title">圆形风格图标</div>
      <div class="icon-list">
        <div class="icon-item" 
          v-for="icon in roundIcons" 
          :key="icon.type" 
          @click="handleIconClick(icon)"
          :title="icon.label"
          draggable="true"
          @dragstart="handleDragStart($event, icon)"
          @dragend="handleDragEnd"
        >
          <component :is="icon.component" :style="{ fontSize: '20px' }" />
        </div>
      </div>
    </div>

    <!-- 简约风格图标组 -->
    <div class="icon-group">
      <div class="icon-title">简约风格图标</div>
      <div class="icon-list">
        <div class="icon-item" 
          v-for="icon in simpleIcons" 
          :key="icon.type" 
          @click="handleIconClick(icon)"
          :title="icon.label"
          draggable="true"
          @dragstart="handleDragStart($event, icon)"
          @dragend="handleDragEnd"
        >
          <component :is="icon.component" />
        </div>
      </div>
    </div>

    <!-- 手绘风格图标组 -->
    <div class="icon-group">
      <div class="icon-title">趣味风格图标</div>
      <div class="icon-list">
        <div class="icon-item" 
          v-for="icon in handpaintedIcons" 
          :key="icon.type" 
          @click="handleIconClick(icon)"
          :title="icon.label"
          draggable="true"
          @dragstart="handleDragStart($event, icon)"
          @dragend="handleDragEnd"
        >
          <component :is="icon.component" :icon="icon.icon" width="24" height="24" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, h } from 'vue'
// Icon Park 其他风格图标
import {
  UserBusiness, PhoneIncoming, MailPackage, LocalPin, DegreeHat, BuildingOne, Trophy, Certificate, ImageFiles, EditTwo,
  People, PhoneIncomingOne, EmailPush, BookOne, Workbench, LightMember, PictureOne, EditOne
} from '@icon-park/vue-next'

// Tabler 简约风格图标
import {
  UserCircle,
  Phone,
  Mail,
  MapPin,
  School as TablerSchool,
  Building as TablerBuilding,
  Award,
  Certificate as TablerCertificate,
  Photo,
  Edit as TablerEdit
} from '@vicons/tabler'

// Iconify 组件用于多彩图标
import { Icon } from '@iconify/vue'

// Ant Design 实心风格图标
import {
  ContactsFilled,
  PhoneFilled,
  MailFilled,
  EnvironmentFilled,
  ReadFilled,
  BankFilled,
  StarFilled,
  TrophyFilled,
  PictureFilled,
  EditFilled
} from '@ant-design/icons-vue'

// Ionicons 5 圆形风格图标
import {
  PersonCircle,
  CallSharp,
  MailSharp,
  LocationSharp,
  SchoolSharp,
  BusinessSharp,
  StarSharp,
  RibbonSharp,
  ImagesSharp,
  CreateSharp
} from '@vicons/ionicons5'

// Carbon 圆形风格图标
import {
  UserAvatar,
  Phone as CarbonPhone,
  Email,
  Location,
  Education,
  Enterprise,
  Star as CarbonStar,
  Certificate as CarbonCertificate,
  ImageMedical,
  Edit as CarbonEdit
} from '@vicons/carbon'

const emit = defineEmits(['select-icon'])

// 图标主题类型
const themes = {
  filled: 'filled',
  outline: 'outline',
  colorful: 'multi-color',
  handpainted: 'hand-painted'
}

// 实心风格图标（使用 Ionicons 5）
const filledIcons = [
  { type: 'user-filled', component: PersonCircle, label: '用户' },
  { type: 'phone-filled', component: CallSharp, label: '电话' },
  { type: 'email-filled', component: MailSharp, label: '邮箱' },
  { type: 'address-filled', component: LocationSharp, label: '地址' },
  { type: 'education-filled', component: SchoolSharp, label: '教育' },
  { type: 'work-filled', component: BusinessSharp, label: '工作' },
  { type: 'skill-filled', component: StarSharp, label: '技能' },
  { type: 'certificate-filled', component: RibbonSharp, label: '证书' },
  { type: 'portfolio-filled', component: ImagesSharp, label: '作品' },
  { type: 'edit-filled', component: CreateSharp, label: '编辑' }
]

// 线框风格图标
const outlineIcons = [
  { type: 'user-outline', component: UserBusiness, label: '用户' },
  { type: 'phone-outline', component: PhoneIncoming, label: '电话' },
  { type: 'email-outline', component: MailPackage, label: '邮箱' },
  { type: 'address-outline', component: LocalPin, label: '地址' },
  { type: 'education-outline', component: DegreeHat, label: '教育' },
  { type: 'work-outline', component: BuildingOne, label: '工作' },
  { type: 'skill-outline', component: Trophy, label: '技能' },
  { type: 'certificate-outline', component: Certificate, label: '证书' },
  { type: 'portfolio-outline', component: ImageFiles, label: '作品' },
  { type: 'edit-outline', component: EditTwo, label: '编辑' }
]

// 多彩风格图标（使用 Iconify）
const colorfulIcons = [
  { type: 'user-colorful', component: Icon, icon: 'twemoji:bust-in-silhouette', label: '用户' },
  { type: 'phone-colorful', component: Icon, icon: 'twemoji:telephone-receiver', label: '电话' },
  { type: 'email-colorful', component: Icon, icon: 'twemoji:envelope', label: '邮箱' },
  { type: 'address-colorful', component: Icon, icon: 'twemoji:round-pushpin', label: '地址' },
  { type: 'education-colorful', component: Icon, icon: 'twemoji:graduation-cap', label: '教育' },
  { type: 'work-colorful', component: Icon, icon: 'twemoji:office-building', label: '工作' },
  { type: 'skill-colorful', component: Icon, icon: 'twemoji:star', label: '技能' },
  { type: 'certificate-colorful', component: Icon, icon: 'twemoji:scroll', label: '证书' },
  { type: 'portfolio-colorful', component: Icon, icon: 'twemoji:framed-picture', label: '作品' },
  { type: 'edit-colorful', component: Icon, icon: 'twemoji:pencil', label: '编辑' }
]

// 圆形风格图标（使用 Carbon）
const roundIcons = [
  { type: 'user-round', component: UserAvatar, label: '用户' },
  { type: 'phone-round', component: CarbonPhone, label: '电话' },
  { type: 'email-round', component: Email, label: '邮箱' },
  { type: 'address-round', component: Location, label: '地址' },
  { type: 'education-round', component: Education, label: '教育' },
  { type: 'work-round', component: Enterprise, label: '工作' },
  { type: 'skill-round', component: CarbonStar, label: '技能' },
  { type: 'certificate-round', component: CarbonCertificate, label: '证书' },
  { type: 'portfolio-round', component: ImageMedical, label: '作品' },
  { type: 'edit-round', component: CarbonEdit, label: '编辑' }
]

// 简约风格图标（使用 Tabler）
const simpleIcons = [
  { type: 'user-simple', component: UserCircle, label: '用户' },
  { type: 'phone-simple', component: Phone, label: '电话' },
  { type: 'email-simple', component: Mail, label: '邮箱' },
  { type: 'address-simple', component: MapPin, label: '地址' },
  { type: 'education-simple', component: TablerSchool, label: '教育' },
  { type: 'work-simple', component: TablerBuilding, label: '工作' },
  { type: 'skill-simple', component: Award, label: '技能' },
  { type: 'certificate-simple', component: TablerCertificate, label: '证书' },
  { type: 'portfolio-simple', component: Photo, label: '作品' },
  { type: 'edit-simple', component: TablerEdit, label: '编辑' }
]

// 手绘风格图标（使用 noto-emoji 和 line-md）
const handpaintedIcons = [
  { type: 'user-fun', component: Icon, icon: 'noto:artist-palette', label: '用户' },
  { type: 'phone-fun', component: Icon, icon: 'line-md:phone-call-twotone', label: '电话' },
  { type: 'email-fun', component: Icon, icon: 'line-md:email-twotone', label: '邮箱' },
  { type: 'address-fun', component: Icon, icon: 'noto:world-map', label: '地址' },
  { type: 'education-fun', component: Icon, icon: 'noto:graduation-cap', label: '教育' },
  { type: 'work-fun', component: Icon, icon: 'line-md:computer-twotone', label: '工作' },
  { type: 'skill-fun', component: Icon, icon: 'noto:sparkles', label: '技能' },
  { type: 'certificate-fun', component: Icon, icon: 'noto:scroll', label: '证书' },
  { type: 'portfolio-fun', component: Icon, icon: 'line-md:image-twotone', label: '作品' },
  { type: 'edit-fun', component: Icon, icon: 'line-md:edit-twotone', label: '编辑' }
]

const handleIconClick = (icon) => {
  emit('select-icon', {
    type: icon.type,
    component: icon.component.name,
    props: {
      theme: icon.theme,
      size: 20
    }
  })
}

// 添加 svg-icon 组件
const SvgIcon = {
  props: {
    component: Object,
    size: Number
  },
  render() {
    return h(this.component, {
      style: {
        width: `${this.size}px`,
        height: `${this.size}px`
      }
    })
  }
}

// 在 script setup 中添加拖拽事件处理函数
const handleDragStart = (event, icon) => {
  event.dataTransfer.effectAllowed = 'copy'
  event.dataTransfer.dropEffect = 'copy'
  
  // 根据不同类型的图标构建不同的数据
  let iconData = {
    type: 'icon',
    data: {
      iconType: icon.type,
      component: icon.component.name
    }
  }

  // 根据图标类型添加特定属性
  if (icon.theme) {
    iconData.data.theme = icon.theme
  }
  
  if (icon.icon) {
    iconData.data.icon = icon.icon
  }

  // 设置默认大小
  iconData.data.size = 20

  event.dataTransfer.setData('application/json', JSON.stringify(iconData))
  event.target.classList.add('dragging')
}

const handleDragEnd = (event) => {
  // 移除拖拽时的视觉反馈
  event.target.classList.remove('dragging')
}
</script>

<style scoped>
.icon-panel {
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
}

.icon-group {
  margin-bottom: 16px;
}

.icon-title {
  font-size: 13px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
  padding-left: 4px;
  border-left: 3px solid #1890ff;
}

.icon-list {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: grab;
  transition: all 0.2s ease;
}

.icon-item.dragging {
  opacity: 0.5;
  cursor: grabbing;
}

.icon-item:hover {
  background-color: #f0f7ff;
  border-color: #91caff;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(24, 144, 255, 0.1);
}

.icon-item:hover .icon-label {
  color: #1890ff;
}

.icon-item :deep(svg) {
  width: 20px;
  height: 20px;
  color: #666;
  transition: color 0.2s ease;
}

.icon-item:hover :deep(svg) {
  color: #1890ff;
}
</style> 