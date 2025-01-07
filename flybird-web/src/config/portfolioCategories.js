import {
  HomeIcon,
  DevicePhoneMobileIcon,
  SwatchIcon,
  GlobeAltIcon,
  FilmIcon,
  VideoCameraIcon,
  AcademicCapIcon,
  Square2StackIcon,
  CubeIcon,
  SparklesIcon,
  UserGroupIcon,
  CameraIcon,
  PhotoIcon,
  FireIcon,
  ClockIcon,
  PaintBrushIcon
} from '@heroicons/vue/24/outline'

// 先定义 portfolioCategories
export const portfolioCategories = {
  discover: {
    title: '发现优秀作品',
    description: '探索来自全球创意社区的优秀作品',
    categories: [
      {
        id: 'all',
        name: '全部',
        icon: HomeIcon
      },
      {
        id: 'ui',
        name: 'UI设计',
        icon: DevicePhoneMobileIcon,
        children: [
          { id: 'mobile', name: '移动端' },
          { id: 'web', name: '网页' },
          { id: 'desktop', name: '桌面端' }
        ]
      },
      {
        id: 'graphic',
        name: '平面设计',
        icon: PaintBrushIcon,
        children: [
          { id: 'poster', name: '海报' },
          { id: 'brand', name: '品牌' },
          { id: 'print', name: '印刷' }
        ]
      },
      { id: 'popular', name: '热门', icon: FireIcon },
      { id: 'latest', name: '最新', icon: ClockIcon },
      { id: 'following', name: '关注', icon: UserGroupIcon }
    ]
  },
  design: {
    title: '设计作品',
    description: '展示优秀的设计作品，分享设计灵感',
    categories: [
      { id: 'all', name: '全部', icon: HomeIcon },
      {
        id: 'ui',
        name: 'UI设计',
        icon: DevicePhoneMobileIcon,
        children: [
          { id: 'mobile', name: '移动端' },
          { id: 'web', name: '网页端' },
          { id: 'desktop', name: '桌面端' }
        ]
      },
      {
        id: 'graphic',
        name: '平面设计',
        icon: SwatchIcon,
        children: [
          { id: 'poster', name: '海报' },
          { id: 'brand', name: '品牌' },
          { id: 'packaging', name: '包装' }
        ]
      },
      {
        id: 'web',
        name: 'Web设计',
        icon: GlobeAltIcon,
        children: [
          { id: 'website', name: '网站设计' },
          { id: 'landing', name: '落地页' },
          { id: 'admin', name: '后台系统' }
        ]
      }
    ]
  },
  video: {
    title: '视频作品',
    description: '分享创意视频作品，展现独特视角',
    categories: [
      { id: 'all', name: '全部', icon: HomeIcon },
      {
        id: 'commercial',
        name: '商业广告',
        icon: FilmIcon,
        children: [
          { id: 'product', name: '产品广告' },
          { id: 'brand', name: '品牌广告' },
          { id: 'service', name: '服务广告' }
        ]
      },
      {
        id: 'vlog',
        name: '生活记录',
        icon: VideoCameraIcon,
        children: [
          { id: 'daily', name: '日常生活' },
          { id: 'travel', name: '旅行' },
          { id: 'food', name: '美食' }
        ]
      },
      {
        id: 'tutorial',
        name: '教程',
        icon: AcademicCapIcon,
        children: [
          { id: 'software', name: '软件教程' },
          { id: 'skill', name: '技能教学' },
          { id: 'diy', name: 'DIY教程' }
        ]
      }
    ]
  },
  animation: {
    title: '动画作品',
    description: '展示创意动画作品，分享动画技巧',
    categories: [
      { id: 'all', name: '全部', icon: HomeIcon },
      {
        id: '2d',
        name: '2D动画',
        icon: Square2StackIcon,
        children: [
          { id: 'motion', name: '动态图形' },
          { id: 'character', name: '角色动画' },
          { id: 'explainer', name: '解释动画' }
        ]
      },
      {
        id: '3d',
        name: '3D动画',
        icon: CubeIcon,
        children: [
          { id: '3d-character', name: '角色动画' },
          { id: 'product', name: '产品动画' },
          { id: 'architectural', name: '建筑动画' }
        ]
      },
      {
        id: 'interactive',
        name: '交互动画',
        icon: SparklesIcon,
        children: [
          { id: 'ui', name: 'UI动效' },
          { id: 'web', name: '网页动画' },
          { id: 'game', name: '游戏动画' }
        ]
      }
    ]
  },
  photo: {
    title: '摄影作品',
    description: '展示精美摄影作品，分享摄影技巧',
    categories: [
      { id: 'all', name: '全部', icon: HomeIcon },
      {
        id: 'landscape',
        name: '风景摄影',
        icon: CameraIcon,
        children: [
          { id: 'mountain', name: '山景' },
          { id: 'sea', name: '海景' },
          { id: 'city', name: '城市' }
        ]
      },
      {
        id: 'portrait',
        name: '人像摄影',
        icon: PhotoIcon,
        children: [
          { id: 'studio', name: '工作室' },
          { id: 'street', name: '街头' },
          { id: 'fashion', name: '时尚' }
        ]
      },
      {
        id: 'animal',
        name: '动物摄影',
        icon: CameraIcon,
        children: [
          { id: 'wildlife', name: '野生动物' },
          { id: 'pet', name: '宠物' },
          { id: 'reptile', name: '爬行动物' }
        ]
      }
    ]
  }
}

// 然后定义 mainCategories
export const mainCategories = [
  { 
    name: '发现', 
    path: '/portfolio', 
    icon: HomeIcon,
    type: 'discover'
  },
  { 
    name: '设计', 
    path: '/portfolio/design', 
    icon: PaintBrushIcon,
    type: 'design'
  },
  { 
    name: '视频', 
    path: '/portfolio/video', 
    icon: VideoCameraIcon,
    type: 'video'
  },
  { 
    name: '动画', 
    path: '/portfolio/animation', 
    icon: FilmIcon,
    type: 'animation'
  },
  { 
    name: '摄影', 
    path: '/portfolio/photo', 
    icon: CameraIcon,
    type: 'photo'
  }
]

// 修改生成菜单组的函数
export function generateMenuGroups(type) {
  return [
    {
      title: `${portfolioCategories[type].title}分类`,
      items: mainCategories.map(category => ({
        name: category.name,
        path: category.path,
        icon: category.icon
      }))
    }
  ]
} 