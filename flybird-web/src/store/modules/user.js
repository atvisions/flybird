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
  // ... 其他 actions 保持不变
} 