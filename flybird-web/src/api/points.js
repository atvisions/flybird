import request from '@/utils/request'

// 获取积分信息
export function getPointsInfo() {
  return request({
    url: '/api/v1/membership/points/balance/',
    method: 'get'
  })
}

// 获取积分记录
export function getPointsRecords(params) {
  return request({
    url: '/api/v1/membership/points/records/',
    method: 'get',
    params
  })
}

// 获取签到状态
export function getSignInStatus() {
  return request({
    url: '/api/v1/membership/points/check-in/status/',
    method: 'get'
  })
}

// 签到
export function signIn() {
  return request({
    url: '/api/v1/membership/points/check-in/',
    method: 'post'
  })
}

// 获取订单列表
export function getOrders() {
  return request({
    url: '/api/v1/membership/orders/',
    method: 'get'
  })
} 