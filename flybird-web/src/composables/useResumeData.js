import { ref } from 'vue'

export function useResumeData() {
  const templates = ref([
    {
      id: 1,
      title: '简约风格简历模板',
      category: 'fresh',
      cover: 'https://picsum.photos/600/800?random=1',
      author: {
        name: '张小明',
        avatar: 'https://picsum.photos/32/32?random=1'
      },
      views: 1234,
      likes: 89,
      downloads: 456,
      isPro: false,
      date: '2024-03-15'
    },
    {
      id: 2,
      title: '专业商务简历模板',
      category: 'experienced',
      cover: 'https://picsum.photos/600/800?random=2',
      author: {
        name: '李晓华',
        avatar: 'https://picsum.photos/32/32?random=2'
      },
      views: 856,
      likes: 67,
      downloads: 234,
      isPro: true,
      date: '2024-03-14'
    },
    {
      id: 3,
      title: '创意设计师简历模板',
      category: 'creative',
      cover: 'https://picsum.photos/600/800?random=3',
      author: {
        name: '王大力',
        avatar: 'https://picsum.photos/32/32?random=3'
      },
      views: 2341,
      likes: 178,
      downloads: 567,
      isPro: true,
      date: '2024-03-13'
    },
    {
      id: 4,
      title: '管理层高端简历模板',
      category: 'manager',
      cover: 'https://picsum.photos/600/800?random=4',
      author: {
        name: '赵明',
        avatar: 'https://picsum.photos/32/32?random=4'
      },
      views: 1567,
      likes: 92,
      downloads: 345,
      isPro: true,
      date: '2024-03-12'
    },
    {
      id: 5,
      title: '国际化英文简历模板',
      category: 'international',
      cover: 'https://picsum.photos/600/800?random=5',
      author: {
        name: '陈小红',
        avatar: 'https://picsum.photos/32/32?random=5'
      },
      views: 987,
      likes: 45,
      downloads: 123,
      isPro: false,
      date: '2024-03-11'
    },
    {
      id: 6,
      title: '应届生求职简历模板',
      category: 'fresh',
      cover: 'https://picsum.photos/600/800?random=6',
      author: {
        name: '刘艺',
        avatar: 'https://picsum.photos/32/32?random=6'
      },
      views: 765,
      likes: 34,
      downloads: 234,
      isPro: false,
      date: '2024-03-10'
    },
    {
      id: 7,
      title: '高级工程师简历模板',
      category: 'experienced',
      cover: 'https://picsum.photos/600/800?random=7',
      author: {
        name: '周工',
        avatar: 'https://picsum.photos/32/32?random=7'
      },
      views: 543,
      likes: 28,
      downloads: 167,
      isPro: true,
      date: '2024-03-09'
    },
    {
      id: 8,
      title: '创意总监简历模板',
      category: 'manager',
      cover: 'https://picsum.photos/600/800?random=8',
      author: {
        name: '林设计',
        avatar: 'https://picsum.photos/32/32?random=8'
      },
      views: 876,
      likes: 56,
      downloads: 289,
      isPro: true,
      date: '2024-03-08'
    }
  ])

  return {
    templates
  }
} 