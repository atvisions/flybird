import axios from 'axios'
import { STORAGE_KEYS } from '@/utils/storage'
import config from '@/config'

const service = axios.create({
  baseURL: config.API_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json'
  },
  retry: 2,
  retryDelay: 1000
})

// 添加重试拦截器
service.interceptors.response.use(undefined, async (err) => {
  const config = err.config;
  
  // 如果配置不存在或未设置重试选项，直接返回错误
  if (!config || !config.retry) {
    return Promise.reject(err);
  }
  
  // 设置重试次数
  config.__retryCount = config.__retryCount || 0;
  
  // 检查是否已超过重试次数
  if (config.__retryCount >= config.retry) {
    return Promise.reject(err);
  }
  
  // 增加重试次数
  config.__retryCount += 1;
  console.log(`正在重试请求 (${config.__retryCount}/${config.retry})`);
  
  // 创建新的 Promise 来处理重试延迟
  const backoff = new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    }, config.retryDelay || 3000);
  });
  
  // 等待延迟后重试请求
  await backoff;
  return service(config);
});

// 请求拦截器
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN)
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response
  },
  error => {
    return Promise.reject(error)
  }
)

export default service