export default {
  userAvatar: state => {
    return state.basicInfo?.avatar || '/default-avatar.png'
  },

  userName: state => {
    // 优先显示用户的 username
    if (state.userInfo?.username) {
      return state.userInfo.username
    }
    // 如果没有 username，显示脱敏的手机号
    if (state.userInfo?.phone) {
      return state.userInfo.phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
    }
    return '未设置昵称'
  },

  userPhone: state => {
    return state.basicInfo?.phone || state.userInfo?.phone
  },

  profileCompleteness: state => {
    return state.completeness || 0
  }
} 