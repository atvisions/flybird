import request from '@/utils/request'

// 获取会员等级列表
export function getTiers() {
  return request({
    url: '/api/v1/membership/tiers/',
    method: 'get'
  })
}

// 创建订单
export function createOrder(data) {
  return request({
    url: '/api/v1/membership/orders/',
    method: 'post',
    data
  })
}

// 创建支付
export function createPayment(data) {
  return request({
    url: '/api/v1/membership/payment/create/',
    method: 'post',
    data
  })
}

// 验证支付状态
export function verifyPayment(orderNo) {
  return request({
    url: '/api/v1/membership/payment/verify/',
    method: 'post',
    data: {
      order_no: orderNo
    }
  })
}

// 获取积分信息
export function getPointsInfo() {
  return request({
    url: '/api/v1/membership/points/balance/',
    method: 'get'
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

// 获取积分记录
export function getPointsRecords(params) {
  return request({
    url: '/api/v1/membership/points/records/',
    method: 'get',
    params
  })
}

// 获取订单记录
export function getOrders() {
  return request({
    url: '/api/v1/membership/orders/',
    method: 'get'
  })
}