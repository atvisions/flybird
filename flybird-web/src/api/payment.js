import request from '@/utils/request'

// 获取会员套餐列表
export function getProPlans() {
  return request({
    url: '/api/v1/payment/plans',
    method: 'get'
  })
}

// 创建支付订单
export function createOrder(data) {
  return request({
    url: '/api/v1/payment/create_order',
    method: 'post',
    data
  })
}

// 查询支付状态
export function queryOrderStatus(orderId) {
  return request({
    url: `/api/v1/payment/order_status/${orderId}`,
    method: 'get'
  })
} 