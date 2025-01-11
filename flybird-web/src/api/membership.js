import request from '@/utils/request'

export const membership = {
  // 获取会员等级列表
  getTiers: () => {
    return request.get('/api/v1/membership/tiers/')
  },
  
  // 创建会员订单
  createOrder: (data) => {
    return request.post('/api/v1/membership/orders/', {
      tier_id: data.tier_id,
      duration: data.duration,
      payment_method: data.payment_method
    })
  },
  
  // 创建支付
  createPayment: (data) => {
    return request.post('/api/v1/membership/payment/create/', {
      order_no: data.order_no,
      payment_method: data.payment_method
    })
  },

  // 获取用户会员信息
  getUserMembership: () => {
    return request.get('/api/v1/membership/membership/')
  },

  // 获取积分信息
  getPoints: () => {
    return request.get('/api/v1/membership/points/')
  },

  // 获取积分记录
  getPointRecords: () => {
    return request.get('/api/v1/membership/points/records/')
  },

  // 验证支付状态
  verifyPayment: (orderNo) => {
    return request.post('/api/v1/membership/payment/verify/', {
      order_no: orderNo
    })
  }
} 