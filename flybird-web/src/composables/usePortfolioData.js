import { ref } from 'vue'

export function usePortfolioData(type) {
  // 根据类型生成不同的示例数据
  const generateWorks = () => {
    const typeSpecificData = {
      discover: [
        { type: 'ui', title: '智能家居App UI设计', subCategory: 'mobile' },
        { type: 'graphic', title: '2024科技峰会品牌设计', subCategory: 'brand' },
        { type: 'web', title: '电商网站设计', subCategory: 'website' },
        { type: 'video', title: '产品宣传创意视频', subCategory: 'product' },
        { type: 'animation', title: '企业品牌动画', subCategory: 'motion' },
        { type: 'photo', title: '城市建筑摄影', subCategory: 'city' }
      ],
      design: [
        { type: 'ui', title: 'UI设计作品', subCategory: 'mobile' },
        { type: 'graphic', title: '平面设计作品', subCategory: 'poster' },
        { type: 'web', title: 'Web设计作品', subCategory: 'website' }
      ],
      video: [
        { type: 'commercial', title: '商业广告视频', subCategory: 'product' },
        { type: 'vlog', title: '生活Vlog', subCategory: 'daily' },
        { type: 'tutorial', title: '教程视频', subCategory: 'software' }
      ],
      animation: [
        { type: '2d', title: '2D动画作品', subCategory: 'motion' },
        { type: '3d', title: '3D动画作品', subCategory: 'product' },
        { type: 'interactive', title: '交互动画', subCategory: 'ui' }
      ],
      photo: [
        { type: 'landscape', title: '风景摄影', subCategory: 'mountain' },
        { type: 'portrait', title: '人像摄影', subCategory: 'studio' },
        { type: 'animal', title: '动物摄影', subCategory: 'wildlife' }
      ]
    }

    const baseWorks = typeSpecificData[type] || []
    return baseWorks.map((work, index) => ({
      id: index + 1,
      title: work.title,
      type: work.type,
      subCategory: work.subCategory,
      cover: `https://picsum.photos/600/400?random=${index + 1}`,
      author: {
        name: ['张小明', '李晓华', '王大力'][index % 3],
        avatar: `https://picsum.photos/32/32?random=${index + 1}`
      },
      views: Math.floor(Math.random() * 2000) + 500,
      likes: Math.floor(Math.random() * 200) + 50,
      isVideo: ['video', 'animation'].includes(type),
      duration: ['2:35', '1:45', '3:20'][index % 3],
      date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
    }))
  }

  const works = ref(generateWorks())

  return {
    works
  }
} 