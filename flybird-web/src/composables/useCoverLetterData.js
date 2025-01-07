import { ref } from 'vue'

export function useCoverLetterData() {
  const templates = ref([
    {
      id: 1,
      title: '通用求职信模板',
      category: 'general',
      cover: 'https://picsum.photos/600/800?random=11',
      author: {
        name: '张小明',
        avatar: 'https://picsum.photos/32/32?random=11'
      },
      views: 1234,
      likes: 89,
      downloads: 456,
      isPro: false,
      date: '2024-03-15'
    },
    {
      id: 2,
      title: '职业转换求职信',
      category: 'career',
      cover: 'https://picsum.photos/600/800?random=12',
      author: {
        name: '李晓华',
        avatar: 'https://picsum.photos/32/32?random=12'
      },
      views: 856,
      likes: 67,
      downloads: 234,
      isPro: true,
      date: '2024-03-14'
    },
    {
      id: 3,
      title: '学术研究求职信',
      category: 'academic',
      cover: 'https://picsum.photos/600/800?random=13',
      author: {
        name: '王大力',
        avatar: 'https://picsum.photos/32/32?random=13'
      },
      views: 2341,
      likes: 178,
      downloads: 567,
      isPro: true,
      date: '2024-03-13'
    },
    {
      id: 4,
      title: '创意行业求职信',
      category: 'creative',
      cover: 'https://picsum.photos/600/800?random=14',
      author: {
        name: '赵明',
        avatar: 'https://picsum.photos/32/32?random=14'
      },
      views: 1567,
      likes: 92,
      downloads: 345,
      isPro: true,
      date: '2024-03-12'
    }
  ])

  return {
    templates
  }
} 