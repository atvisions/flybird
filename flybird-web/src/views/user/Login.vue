<template>
  <!-- 密码登录表单 -->
  <div v-if="loginType === 'password'">
    <div class="form-group">
      <label class="form-label">账号</label>
      <input
        type="text"
        v-model="form.account"
        placeholder="请输入手机号/邮箱/UID"
        class="form-input"
        :class="{ 'error': errors.account }"
      />
      <div class="error-message" v-if="errors.account">{{ errors.account }}</div>
    </div>
    <!-- ... 其他表单内容 ... -->
  </div>
</template>

<script setup>
const form = reactive({
  account: '',
  password: '',
  code: '',
  remember: false
})

const errors = reactive({
  account: '',
  password: '',
  code: ''
})

// 验证表单
const validateForm = () => {
  let isValid = true
  errors.account = ''
  errors.password = ''

  // 验证账号
  if (!form.account) {
    errors.account = '请输入账号'
    isValid = false
  } else if (!/^1[3-9]\d{9}$/.test(form.account) && 
            !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.account) &&
            !/^\d+$/.test(form.account)) {
    errors.account = '请输入正确的手机号/邮箱/UID'
    isValid = false
  }

  // ... 其他验证逻辑 ...
  return isValid
}

// 处理登录
const handleLogin = async () => {
  if (!validateForm()) return

  try {
    loading.value = true
    const response = await auth.passwordLogin({
      account: form.account,
      password: form.password
    })
    // ... 处理登录成功逻辑 ...
  } catch (error) {
    // ... 处理错误 ...
  }
}
</script> 