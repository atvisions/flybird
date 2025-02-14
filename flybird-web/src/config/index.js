// 导出配置
export default {
  API_URL: process.env.VUE_APP_API_BASE_URL || 'http://192.168.3.22:8000',
  apiPrefix: process.env.VUE_APP_API_PREFIX || '/api',
  mediaURL: process.env.VUE_APP_MEDIA_URL || 'http://192.168.3.22:8000/media',
  socketURL: process.env.VUE_APP_SOCKET_URL || 'ws://192.168.3.22:8000/ws'
} 