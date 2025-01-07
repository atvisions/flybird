import {
  HomeIcon,
  DocumentTextIcon,
  HashtagIcon,
  QuestionMarkCircleIcon,
  CodeBracketIcon,
  ServerIcon,
  DevicePhoneMobileIcon,
  SparklesIcon,
  CogIcon,
  FireIcon,
  BoltIcon,
  BriefcaseIcon,
  WrenchScrewdriverIcon,
  CheckCircleIcon,
  StarIcon,
  GiftIcon
} from '@heroicons/vue/24/outline'

// 主导航分类
export const mainCategories = [
  { name: '首页', path: '/community', icon: HomeIcon },
  { name: '文章', path: '/community/articles', icon: DocumentTextIcon },
  { name: '话题', path: '/community/topics', icon: HashtagIcon },
  { name: '问答', path: '/community/questions', icon: QuestionMarkCircleIcon }
]

// 各页面的分类配置
export const communityCategories = {
  articles: {
    title: '技术文章',
    description: '分享技术经验，共同成长',
    categories: [
      { id: 'all', name: '全部', icon: HomeIcon },
      { id: 'frontend', name: '前端开发', icon: CodeBracketIcon },
      { id: 'backend', name: '后端开发', icon: ServerIcon },
      { id: 'mobile', name: '移动开发', icon: DevicePhoneMobileIcon },
      { id: 'ai', name: '人工智能', icon: SparklesIcon },
      { id: 'devops', name: 'DevOps', icon: CogIcon }
    ]
  },
  topics: {
    title: '热门话题',
    description: '参与技术讨论，表达你的观点',
    categories: [
      { id: 'all', name: '全部', icon: HomeIcon },
      { id: 'hot', name: '热门话题', icon: FireIcon },
      { id: 'tech', name: '技术之争', icon: BoltIcon },
      { id: 'career', name: '职业发展', icon: BriefcaseIcon },
      { id: 'tools', name: '工具推荐', icon: WrenchScrewdriverIcon }
    ]
  },
  questions: {
    title: '问答社区',
    description: '解答技术难题，分享解决方案',
    categories: [
      { id: 'all', name: '全部', icon: HomeIcon },
      { id: 'unsolved', name: '待解决', icon: QuestionMarkCircleIcon },
      { id: 'solved', name: '已解决', icon: CheckCircleIcon },
      { id: 'featured', name: '精选问答', icon: StarIcon },
      { id: 'reward', name: '悬赏问答', icon: GiftIcon }
    ]
  }
} 