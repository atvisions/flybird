import { 
  DocumentTextIcon,
  QuestionMarkCircleIcon,
  HashtagIcon
} from '@heroicons/vue/24/outline'

export const communityMenuGroups = [
  {
    title: '社区',
    items: [
      { 
        name: '文章', 
        path: '/community/articles', 
        icon: DocumentTextIcon 
      },
      { 
        name: '问答', 
        path: '/community/questions', 
        icon: QuestionMarkCircleIcon 
      },
      { 
        name: '话题', 
        path: '/community/topics', 
        icon: HashtagIcon 
      }
    ]
  }
] 