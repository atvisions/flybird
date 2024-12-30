const getters = {
  // ... 其他 getters
  getUserInfo: state => state.user.userInfo,
  getUserAvatar: state => state.user.userInfo?.avatar || '/default-avatar.png'
}

export default getters 