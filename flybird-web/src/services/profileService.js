import { basicProfile, workExperience, jobIntention, optimization, layout } from '@/api/profile'

// 用户资料服务
export const profileService = {
  // 基本信息
  async getBasicInfo() {
    return basicProfile.getBasicInfo()
  },

  async updateBasicInfo(data) {
    return basicProfile.updateBasicInfo(data)
  },

  async uploadAvatar(file) {
    return basicProfile.uploadAvatar(file)
  },

  // 工作经历
  async getWorkExperiences() {
    return workExperience.list()
  },

  async addWorkExperience(data) {
    return workExperience.add(data)
  },

  async updateWorkExperience(id, data) {
    return workExperience.update(id, data)
  },

  async deleteWorkExperience(id) {
    return workExperience.delete(id)
  },

  // 求职意向
  async getJobIntention() {
    return jobIntention.get()
  },

  async updateJobIntention(data) {
    return jobIntention.update(data)
  },

  // 简历优化
  async getOptimizationPreview() {
    return optimization.getPreview()
  },

  async confirmOptimization(id) {
    return optimization.confirm(id)
  },

  async getOptimizationCount() {
    return optimization.getCount()
  },

  // 布局配置
  async updateLayout(data) {
    return layout.update(data)
  },

  // 获取完整度
  async getCompleteness() {
    try {
      const response = await basicProfile.getCompleteness()
      if (response.data?.code === 200) {
        return response.data.data
      }
      throw new Error(response.data?.message || '获取完整度失败')
    } catch (error) {
      console.error('获取完整度失败:', error)
      throw error
    }
  }
} 