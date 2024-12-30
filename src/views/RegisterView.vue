<script setup>
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { register, sendSmsCode } from '@/api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const form = ref({
  phone: '',
  code: '',
  password: ''
})

const countdown = ref(0)
const timer = ref(null)

// 验证手机号格式
const validatePhone = (phone) => {
  return /^1[3-9]\d{9}$/.test(phone)
}

// 发送验证码
const handleSendCode = async () => {
  try {
    // 验证手机号
    if (!validatePhone(form.value.phone)) {
      ElMessage.error('请输入正确的手机号')
      return
    }

    const response = await sendSmsCode({
      phone: form.value.phone,
      scene: 'register'
    })
    
    if (response.data.code === 200) {
      ElMessage.success('验证码已发送')
      // 开始倒计时
      countdown.value = 60
      timer.value = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) {
          clearInterval(timer.value)
        }
      }, 1000)
      
      // 如果是开发环境，显示验证码
      if (response.data.data?.code) {
        ElMessage.info(`验证码: ${response.data.data.code}`)
      }
    } else {
      throw new Error(response.data.message)
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '发送验证码失败')
  }
}

// 注册
const handleRegister = async () => {
  try {
    // 表单验证
    if (!validatePhone(form.value.phone)) {
      ElMessage.error('请输入正确的手机号')
      return
    }
    if (!form.value.code) {
      ElMessage.error('请输入验证码')
      return
    }
    if (!form.value.password) {
      ElMessage.error('请输入密码')
      return
    }

    const response = await register({
      phone: form.value.phone,
      code: form.value.code,
      password: form.value.password
    })
    
    if (response.data.code === 200) {
      ElMessage.success('注册成功')
      localStorage.setItem('access_token', response.data.data.access)
      localStorage.setItem('refresh_token', response.data.data.refresh)
      router.push('/')
    } else {
      throw new Error(response.data.message)
    }
  } catch (error) {
    // 显示具体的错误信息
    const errorMsg = error.response?.data?.errors?.phone || 
                    error.response?.data?.errors?.code ||
                    error.response?.data?.message ||
                    '注册失败'
    ElMessage.error(errorMsg)
  }
}

// 组件销毁时清除定时器
onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})
</script>

<template>
  <div class="register-container">
    <el-form :model="form" label-width="80px">
      <!-- 手机号 -->
      <el-form-item label="手机号">
        <el-input v-model="form.phone" placeholder="请输入手机号" />
      </el-form-item>

      <!-- 验证码 -->
      <el-form-item label="验证码">
        <div class="code-input">
          <el-input v-model="form.code" placeholder="请输入验证码" />
          <el-button 
            :disabled="countdown > 0" 
            @click="handleSendCode"
            class="send-code-btn"
          >
            {{ countdown > 0 ? `${countdown}s后重试` : '发送验证码' }}
          </el-button>
        </div>
      </el-form-item>

      <!-- 密码 -->
      <el-form-item label="密码">
        <el-input 
          v-model="form.password" 
          type="password" 
          placeholder="请输入密码"
        />
      </el-form-item>

      <!-- 注册按钮 -->
      <el-form-item>
        <el-button type="primary" @click="handleRegister">注册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 20px;
}

.code-input {
  display: flex;
  gap: 10px;
}

.send-code-btn {
  white-space: nowrap;
}
</style> 