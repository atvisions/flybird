const config = {
  // 开发环境配置
  development: {
    API_URL: 'http://192.168.2.25:8000',
    API_PREFIX: '/api/v1',
    MEDIA_URL: 'http://192.168.2.25:8000/media',
    SOCKET_URL: 'ws://192.168.2.25:8000/ws'
  },
  // 生产环境配置
  production: {
    API_URL: 'http://www.flybirdx.com:8000',
    API_PREFIX: '/api/v1',
    MEDIA_URL: 'http://www.flybirdx.com:8000/media',
    SOCKET_URL: 'ws://www.flybirdx.com:8000/ws'
  }
}

// 获取当前环境的配置
const env = process.env.NODE_ENV || 'development'
const currentConfig = config[env]

// 导出配置
export default currentConfig

// 为了向后兼容，导出单独的变量
export const { API_URL, API_PREFIX, MEDIA_URL, SOCKET_URL } = currentConfig 