export const API_URL = 'http://192.168.3.16:8000'
export const API_PREFIX = '/api/v1'

// 完整的 API 基础 URL
export const BASE_API_URL = API_URL + API_PREFIX

// 媒体文件 URL
export const MEDIA_URL = process.env.VUE_APP_API_BASE_URL || 'http://192.168.3.16:8000' 