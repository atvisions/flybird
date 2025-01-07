import { ref } from 'vue'

export function useCommunityData() {
  const content = ref([
    {
      id: 1,
      title: '如何使用 Vue 3 Composition API 构建大型应用',
      category: 'frontend',
      cover: 'https://picsum.photos/600/300?random=1',
      author: {
        name: '张小明',
        avatar: 'https://picsum.photos/32/32?random=1'
      },
      views: 1234,
      likes: 89,
      comments: 45,
      isLiked: false,
      isCollected: false,
      date: '2024-03-15'
    },
    {
      id: 2,
      title: 'Node.js 性能优化实践指南',
      category: 'backend',
      cover: 'https://picsum.photos/600/300?random=2',
      author: {
        name: '李晓华',
        avatar: 'https://picsum.photos/32/32?random=2'
      },
      views: 856,
      likes: 67,
      comments: 23,
      isLiked: true,
      isCollected: false,
      date: '2024-03-14'
    },
    {
      id: 3,
      title: '深入理解 React Native 架构设计',
      category: 'mobile',
      cover: 'https://picsum.photos/600/300?random=3',
      author: {
        name: '王大力',
        avatar: 'https://picsum.photos/32/32?random=3'
      },
      views: 2341,
      likes: 178,
      comments: 89,
      isLiked: false,
      isCollected: true,
      date: '2024-03-13'
    }
  ])

  const totalItems = ref(content.value.length)
  const loading = ref(false)
  const hasMore = ref(true)

  const loadMore = async () => {
    loading.value = true
    // 模拟加载更多数据
    await new Promise(resolve => setTimeout(resolve, 1000))
    loading.value = false
  }

  return {
    content,
    totalItems,
    loading,
    hasMore,
    loadMore
  }
} 