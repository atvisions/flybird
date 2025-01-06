const state = {
  token: '',
  refreshToken: '',
  userInfo: {
    data: {
      basic_info: {
        background: null
      }
    }
  }
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_REFRESH_TOKEN: (state, token) => {
    state.refreshToken = token
  },
  SET_USER_INFO: (state, info) => {
    state.userInfo = info
  },
  UPDATE_BACKGROUND: (state, background) => {
    if (!state.userInfo.data) {
      state.userInfo.data = {}
    }
    if (!state.userInfo.data.basic_info) {
      state.userInfo.data.basic_info = {}
    }
    state.userInfo.data.basic_info.background = background
  }
}

const actions = {
  // 登录
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password })
        .then(response => {
          const { data } = response
          commit('SET_TOKEN', data.token)
          setToken(data.token)
          resolve()
        })
        .catch(error => {
          // 处理具体的错误情况
          if (error.response?.data) {
            const errorData = error.response.data
            let errorMessage = '登录失败'

            if (errorData.code === 'user_not_found') {
              errorMessage = '账号不存在'
            } else if (errorData.code === 'invalid_credentials') {
              errorMessage = '密码错误'
            } else if (errorData.code === 'account_disabled') {
              errorMessage = '账号已被禁用'
            } else if (errorData.code === 'account_deleted') {
              errorMessage = '账号已注销'
            } else if (errorData.message) {
              errorMessage = errorData.message
            }

            reject(new Error(errorMessage))
          } else {
            reject(error)
          }
        })
    })
  },
  logout({ commit }) {
    return new Promise((resolve) => {
      // 清理所有相关状态
      commit('SET_TOKEN', '')
      commit('SET_REFRESH_TOKEN', '')
      commit('SET_USER_INFO', null)
      
      // 清理本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('userInfo')
      
      resolve()
    })
  },
  async updateBackground({ commit, dispatch }, formData) {
    try {
      const response = await profile.uploadBackground(formData)
      if (response.data?.code === 200) {
        const background = response.data.data.background
        commit('UPDATE_BACKGROUND', background)
        // 更新完背景后重新获取用户信息
        await dispatch('getUserInfo')
        return background
      }
      throw new Error(response.data?.message || '更新背景图失败')
    } catch (error) {
      console.error('Update background failed:', error)
      throw error
    }
  },
  async getUserInfo({ commit }) {
    try {
      const response = await user.getUserInfo()
      if (response.data?.code === 200) {
        commit('SET_USER_INFO', response.data)
        return response.data
      }
    } catch (error) {
      console.error('Get user info failed:', error)
      throw error
    }
  }
} 