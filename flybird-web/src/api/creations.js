import request from '@/utils/request'

export const creations = {
  getList: (params) => {
    return request({
      url: '/v1/creations/',
      method: 'get',
      params
    })
  },
  
  create: (data) => {
    return request({
      url: '/v1/creations/',
      method: 'post',
      data
    })
  },
  
  update: (id, data) => {
    return request({
      url: `/v1/creations/${id}/`,
      method: 'patch',
      data
    })
  },
  
  delete: (id) => {
    return request({
      url: `/v1/creations/${id}/`,
      method: 'delete'
    })
  }
}