<template>
  <div class="max-w-4xl mx-auto">
    <div class="space-y-6">
      <!-- 账户安全 -->
      <section class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-6 py-4 bg-gray-100 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">账户安全</h2>
        </div>
        
        <div class="p-6 space-y-6">
          <!-- 邮箱 -->
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span class="text-sm font-medium text-gray-900">邮箱</span>
              </div>
              <p class="mt-1 text-sm text-gray-500">{{ email || '未绑定' }}</p>
            </div>
            <button 
              @click="openEmailModal"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-indigo-600 border border-indigo-600 
              hover:bg-indigo-50 transition-colors rounded-md">
              {{ email ? '更换邮箱' : '绑定邮箱' }}
            </button>
          </div>

          <!-- 手机号 -->
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <span class="text-sm font-medium text-gray-900">手机号</span>
              </div>
              <p class="mt-1 text-sm text-gray-500">{{ maskPhone(phone) }}</p>
            </div>
            <button 
              @click="openPhoneModal"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-indigo-600 border border-indigo-600 
              hover:bg-indigo-50 transition-colors rounded-md">
              更换手机号
            </button>
          </div>

          <!-- 密码 -->
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <span class="text-sm font-medium text-gray-900">登录密码</span>
              </div>
              <p class="mt-1 text-sm text-gray-500">用于保护账号安全</p>
            </div>
            <button 
              @click="openPasswordModal"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-indigo-600 border border-indigo-600 
              hover:bg-indigo-50 transition-colors rounded-md">
              修改密码
            </button>
          </div>
        </div>
      </section>

      <!-- 账户注销 -->
      <section class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-6 py-4 bg-gray-100 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">账户注销</h2>
        </div>
        
        <div class="p-6">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2">
                <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                <span class="text-sm font-medium text-gray-900">账户注销</span>
              </div>
              <p class="mt-1 text-sm text-gray-500">注销后，账户将被永久删除且无法恢复</p>
            </div>
            <button 
              @click="openDeleteConfirm"
              :disabled="loading"
              class="text-red-600 hover:text-red-500"
            >
              {{ loading ? '注销中...' : '注销账号' }}
            </button>
          </div>
        </div>
      </section>

      <!-- Teleport 部分重写所有弹窗 -->
      <Teleport to="body">
        <!-- 手机号修改弹窗 -->
        <div v-if="showPhoneModal" class="modal-overlay">
          <div class="modal-content">
            <div class="modal-header">
              <h3>更换手机号</h3>
              <button class="close-btn" @click="closePhoneModal">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="form-group">
                <input 
                  type="text" 
                  v-model="phoneManager.state.value"
                  placeholder="请输入新手机号"
                  :disabled="phoneManager.state.loading"
                />
              </div>
              <div class="form-group">
                <div class="code-input">
                  <input 
                    type="text" 
                    v-model="phoneManager.state.code"
                    placeholder="请输入验证码"
                    :disabled="phoneManager.state.loading"
                  />
                  <button 
                    @click="handlePhoneSendCode"
                    :disabled="phoneManager.state.loading || phoneManager.state.countdown > 0"
                    class="code-btn"
                  >
                    {{ phoneManager.state.countdown > 0 ? `${phoneManager.state.countdown}s` : '获取验证码' }}
                  </button>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closePhoneModal"
                :disabled="phoneManager.state.loading"
              >
                取消
              </button>
              <button 
                class="btn btn-primary" 
                @click="handlePhoneUpdate"
                :disabled="phoneManager.state.loading"
              >
                {{ phoneManager.state.loading ? '更新中...' : '确认' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 密码修改弹窗 -->
        <div v-if="showPasswordModal" class="modal-overlay">
          <div class="modal-content">
            <div class="modal-header">
              <h3>修改密码</h3>
              <button class="close-btn" @click="closePasswordModal">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="form-group">
                <input 
                  type="password" 
                  v-model="password.state.oldPassword"
                  placeholder="请输入原密码"
                  :disabled="password.state.loading"
                />
              </div>
              <div class="form-group">
                <input 
                  type="password" 
                  v-model="password.state.newPassword"
                  placeholder="请输入新密码"
                  :disabled="password.state.loading"
                  @input="handlePasswordInput"
                />
                <div v-if="password.state.error" class="text-sm text-red-500 mt-1">
                  {{ password.state.error }}
                </div>
                
                <!-- 密码强度指示器 -->
                <div class="mt-2">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs text-gray-500">密码强度</span>
                    <span class="text-xs" :class="strengthTextClass">{{ strengthText }}</span>
                  </div>
                  <div class="flex gap-1 h-1">
                    <div 
                      v-for="n in 4" 
                      :key="n"
                      class="flex-1 rounded-full transition-colors duration-200"
                      :class="[
                        n <= password.state.strength 
                          ? strengthColorClass 
                          : 'bg-gray-200'
                      ]"
                    ></div>
                  </div>
                </div>
                
                <!-- 密码规则提示 -->
                <div class="text-xs text-gray-400 mt-2 space-y-1">
                  <div>密码要求：</div>
                  <div>• 长度在8-20个字符之间</div>
                  <div>• 必须包含字母</div>
                  <div>• 必须包含数字</div>
                  <div>• 不能与当前密码相同</div>
                  <div>建议包含（可选）：</div>
                  <div>• 大小写字母</div>
                  <div>• 特殊字符（!@#$%^&*）</div>
                </div>
              </div>
              <div class="form-group">
                <input 
                  type="password" 
                  v-model="password.state.confirmPassword"
                  placeholder="请确认新密码"
                  :disabled="password.state.loading"
                  @input="validateConfirmPassword"
                />
                <div v-if="confirmPasswordError" class="text-sm text-red-500 mt-1">
                  {{ confirmPasswordError }}
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closePasswordModal"
                :disabled="password.state.loading"
              >
                取消
              </button>
              <button 
                class="btn btn-primary" 
                @click="handlePasswordUpdate"
                :disabled="password.state.loading"
              >
                {{ password.state.loading ? '更新中...' : '确认' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 账户注销确认弹窗 -->
        <div v-if="showDeleteConfirm" class="modal-overlay">
          <div class="modal-content">
            <div class="modal-header">
              <div class="flex items-center space-x-2">
                <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <h3 class="text-red-700">账户注销确认</h3>
              </div>
              <button class="close-btn" @click="closeDeleteConfirm">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="bg-red-50 p-4 rounded-md mb-4 border border-red-100">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div class="ml-3">
                    <h3 class="text-sm font-medium text-red-800">
                      请确认以下信息
                    </h3>
                    <div class="mt-2 text-sm text-red-700">
                      <ul class="list-disc pl-5 space-y-1">
                        <li>账户注销后将无法恢复</li>
                        <li>所有个人数据将被永久删除</li>
                        <li>相关服务和功能将立即停止</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <input 
                  type="password" 
                  v-model="deleteForm.password"
                  placeholder="请输入登录密码确认"
                  :disabled="loading"
                  class="border-red-300 focus:border-red-500 focus:ring-red-500"
                />
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closeDeleteConfirm"
                :disabled="loading"
              >
                取消
              </button>
              <button 
                class="btn btn-danger" 
                @click="handleConfirmDelete"
                :disabled="loading || !deleteForm.password"
              >
                {{ loading ? '注销中...' : '确认注销' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 邮箱绑定弹窗 -->
        <div v-if="showEmailModal" class="modal-overlay">
          <div class="modal-content">
            <div class="modal-header">
              <h3>{{ email ? '更换邮箱' : '绑定邮箱' }}</h3>
              <button class="close-btn" @click="closeEmailModal">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="form-group">
                <input 
                  type="email" 
                  v-model="emailManager.state.value"
                  placeholder="请输入邮箱地址"
                  :disabled="emailManager.state.loading"
                />
              </div>
              <div class="form-group">
                <input 
                  type="password" 
                  v-model="emailManager.state.password"
                  placeholder="请输入登录密码"
                  :disabled="emailManager.state.loading"
                />
              </div>
              <div class="form-group">
                <div class="code-input">
                  <input 
                    type="text" 
                    v-model="emailManager.state.code"
                    placeholder="请输入验证码"
                    :disabled="emailManager.state.loading"
                  />
                  <button 
                    @click="handleEmailSendCode"
                    :disabled="isCodeButtonDisabled"
                    class="code-btn"
                  >
                    {{ emailManager.state.countdown > 0 
                      ? `${emailManager.state.countdown}s` 
                      : (isRequestingCode ? '发送中...' : '获取验证码') 
                    }}
                  </button>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closeEmailModal"
                :disabled="emailManager.state.loading"
              >
                取消
              </button>
              <button 
                class="btn btn-primary" 
                @click="handleEmailUpdate"
                :disabled="!isEmailFormValid"
              >
                {{ emailManager.state.loading ? (email ? '更换中...' : '绑定中...') : '确认' }}
              </button>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { showToast } from '@/components/ToastMessage'
import { useDeleteAccount } from '@/composables/useDeleteAccount'
import { useNickname } from '@/composables/useNickname'
import { usePhone } from '@/composables/usePhone'
import { useEmail } from '@/composables/useEmail'
import { useChangePassword } from '@/composables/useChangePassword'
import { ElMessageBox } from 'element-plus'
import { account } from '@/api/account'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

const store = useStore()
const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()
// 基础信息
const username = computed(() => userStore.userInfo?.username || '未设置')
const uid = computed(() => userStore.userInfo?.uid || '暂无')
const phone = computed(() => userStore.userInfo?.phone || '')
const email = computed(() => userStore.userInfo?.email || '')

// 使用 composables
const nickname = useNickname()
const phoneManager = usePhone()
const emailManager = useEmail()
const { deleteLoading: loading, handleDeleteAccount } = useDeleteAccount()
const password = useChangePassword()

// 工具方法
const maskPhone = (phone) => {
  if (!phone) return '未绑定'
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

// 弹窗状态
const showPhoneModal = ref(false)
const showPasswordModal = ref(false)
const showDeleteConfirm = ref(false)

// 打开弹窗的方法
const openPhoneModal = () => {
  phoneManager.state.value = ''
  phoneManager.state.code = ''
  showPhoneModal.value = true
}

const openPasswordModal = () => {
  showPasswordModal.value = true
}

const openDeleteConfirm = async () => {
  showDeleteConfirm.value = true
}

// 关闭弹窗的方法
const closePhoneModal = () => {
  showPhoneModal.value = false
  phoneManager.state.value = ''
  phoneManager.state.code = ''
}

const closePasswordModal = () => {
  showPasswordModal.value = false
}

const closeDeleteConfirm = () => {
  showDeleteConfirm.value = false
  deleteForm.value.password = ''
}

// 处理成功回调
const handlePasswordSuccess = () => {
  closePasswordModal()
  showToast('密码修改成功', 'success')
}


// 添加密码验证相关的状态和方法
const confirmPasswordError = ref('')

const validateNewPassword = () => {
  // 使用 composable 中的验证方法
  password.state.error = password.validatePassword(password.state.newPassword)
  // 如果新密码变化，也要检查确认密码
  if (password.state.confirmPassword) {
    validateConfirmPassword()
  }
}

const validateConfirmPassword = () => {
  if (!password.state.confirmPassword) {
    confirmPasswordError.value = ''
  } else if (password.state.confirmPassword !== password.state.newPassword) {
    confirmPasswordError.value = '两次输入的密码不一致'
  } else {
    confirmPasswordError.value = ''
  }
}

// 处理密码更新
const handlePasswordUpdate = async () => {
  // 先验证一次
  validateNewPassword()
  validateConfirmPassword()
  
  // 如果有错误就不提交
  if (password.state.error || confirmPasswordError.value) {
    return
  }
  
  try {
    userInfoLoading.value = true
    const response = await account.updatePassword({
      old_password: password.state.oldPassword,
      new_password: password.state.newPassword,
      confirm_password: password.state.confirmPassword
    })
    
    if (response?.data?.code === 200) {
      closePasswordModal()
      showToast('密码修改成功', 'success')
      // 清空表单
      password.state.oldPassword = ''
      password.state.newPassword = ''
      password.state.confirmPassword = ''
    }
  } catch (error) {
    console.error('密码修改失败:', error)
    showToast(error?.response?.data?.message || '密码修改失败', 'error')
  } finally {
    userInfoLoading.value = false
  }
}

// 处理手机号更新
const handlePhoneUpdate = async () => {
  if (!phoneManager.state.value || !phoneManager.state.code) {
    showToast('请填写完整信息', 'warning')
    return
  }

  try {
    const response = await account.changePhone({
      phone: phoneManager.state.value,
      code: phoneManager.state.code
    })
    
    if (response?.data?.code === 200) {
      closePhoneModal()
      await userStore.getUserInfo()
      showToast('手机号更新成功', 'success')
    } else {
      throw new Error(response?.data?.message || '手机号更新失败')
    }
  } catch (error) {
    console.error('手机号更新失败:', error)
    const errorMsg = error.response?.data?.message || 
                    error.response?.data?.detail ||
                    error.message || 
                    '手机号更新失败'
    showToast(errorMsg, 'error')
  }
}

// 邮箱相关
const showEmailModal = ref(false)

const openEmailModal = () => {
  emailManager.state.value = ''
  emailManager.state.code = ''
  showEmailModal.value = true
}

const closeEmailModal = () => {
  showEmailModal.value = false
  emailManager.state.value = ''
  emailManager.state.code = ''
  emailManager.state.password = ''
}

const handleEmailUpdate = async () => {
  try {
    const data = {
      email: emailManager.state.value,
      code: emailManager.state.code,
      password: emailManager.state.password
    }
    
    // 根据是否已有邮箱决定是绑定还是更换
    const response = await (email.value ? 
      account.changeEmail(data) : 
      account.bindEmail(data))

    if (response?.data?.message) {
      closeEmailModal()
      await store.dispatch('getUserInfo')
      showToast(response.data.message, 'success')
    }
  } catch (error) {
    console.error('邮箱更新失败:', error)
    const errorMsg = error.response?.data?.detail || 
                    error.response?.data?.message || 
                    error.message || 
                    '邮箱操作失败'
    showToast(errorMsg, 'error')
  }
}

// 添加计算属性控制邮箱表单按钮状态
const isEmailFormValid = computed(() => {
  // 检查邮箱格式
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  const isValidEmail = emailRegex.test(emailManager.state.value)
  
  // 检查所有必填字段
  return emailManager.state.value && 
         emailManager.state.code && 
         emailManager.state.password &&  // 密码必填
         isValidEmail && 
         !emailManager.state.loading
})

// 添加防重复点击状态
const isRequestingCode = ref(false)

// 处理邮箱更新的验证码发送
const handleEmailSendCode = async () => {
  if (!emailManager.state.value) {
    showToast('请输入新邮箱', 'warning')
    return
  }
  
  if (!phone.value) {
    showToast('当前账号未绑定手机号，无法进行邮箱验证', 'warning')
    return
  }
  
  // 验证邮箱格式
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(emailManager.state.value)) {
    showToast('请输入正确的邮箱格式', 'warning')
    return
  }
  
  try {
    emailManager.state.loading = true
    isRequestingCode.value = true
    const response = await account.sendEmailCode({
      email: emailManager.state.value
    })
    
    if (response?.data?.message) {
      showToast(response.data.message, 'success')
      startEmailCountdown()
    }
  } catch (error) {
    console.error('发送验证码失败:', error)
    const errorMsg = error.response?.data?.detail || 
                    error.message || 
                    '发送验证码失败'
    showToast(errorMsg, 'error')
  } finally {
    emailManager.state.loading = false
    isRequestingCode.value = false
  }
}

// 修改按钮禁用状态
const isCodeButtonDisabled = computed(() => {
  return emailManager.state.loading || 
         emailManager.state.countdown > 0 || 
         !emailManager.state.password || 
         !emailManager.state.value ||
         isRequestingCode.value
})

// 密码强度相关
const strengthText = computed(() => {
  const strength = password.state.strength
  if (strength === 0) return '弱'
  if (strength <= 2) return '中'
  if (strength <= 4) return '强'
  return '非常强'
})

const strengthTextClass = computed(() => {
  const strength = password.state.strength
  if (strength === 0) return 'text-red-500'
  if (strength <= 2) return 'text-yellow-500'
  if (strength <= 4) return 'text-green-500'
  return 'text-green-600'
})

const strengthColorClass = computed(() => {
  const strength = password.state.strength
  if (strength === 0) return 'bg-red-500'
  if (strength <= 2) return 'bg-yellow-500'
  if (strength <= 4) return 'bg-green-500'
  return 'bg-green-600'
})

const handlePasswordInput = () => {
  validateNewPassword()
  password.updatePasswordStrength(password.state.newPassword)
}

// 添加表单数据
const deleteForm = ref({
  password: ''
})

// 处理确认注销
const handleConfirmDelete = async () => {
  if (!deleteForm.value.password) {
    showToast('请输入密码', 'warning')
    return
  }
  
  try {
    const response = await account.deleteAccount(deleteForm.value)
    if (response?.data?.code === 200) {
      showToast('账号已注销', 'success')
      // 使用 auth store 的 logout 方法清除所有状态
      await authStore.logout()
      // 清除 user store 的状态
      userStore.clearUserInfo()
      // 清除其他可能的状态
      localStorage.removeItem('isLoggedIn')
      // 强制刷新页面以确保所有状态都被清除
      window.location.href = '/login'
    }
  } catch (error) {
    console.error('注销失败:', error)
    showToast(error?.message || '注销失败', 'error')
  }
}

// 倒计时管理
const startPhoneCountdown = () => {
  phoneManager.state.countdown = 60
  const timer = setInterval(() => {
    phoneManager.state.countdown--
    if (phoneManager.state.countdown <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const startEmailCountdown = () => {
  emailManager.state.countdown = 60
  const timer = setInterval(() => {
    emailManager.state.countdown--
    if (emailManager.state.countdown <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

// 处理手机号更新的验证码发送
const handlePhoneSendCode = async () => {
  if (!phoneManager.state.value) {
    showToast('请输入新手机号', 'warning')
    return
  }
  
  // 验证手机号格式
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(phoneManager.state.value)) {
    showToast('请输入正确的手机号格式', 'warning')
    return
  }
  
  try {
    phoneManager.state.loading = true
    const response = await account.sendVerifyCode({
      phone: phoneManager.state.value,
      scene: 'change_phone',
      type: 'sms'
    })

    if (response?.data?.code === 200) {
      startPhoneCountdown()
      showToast('验证码已发送', 'success')
    } else {
      throw new Error(response?.data?.message || '发送验证码失败')
    }
  } catch (error) {
    console.error('发送验证码失败:', error)
    const errorMsg = error.response?.data?.message || 
                    error.response?.data?.detail ||
                    error.message || 
                    '发送验证码失败'
    showToast(errorMsg, 'error')
  } finally {
    phoneManager.state.loading = false
  }
}

// 表单数据
const form = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// 用户信息
const userInfo = ref(null)

// 用户信息加载状态
const userInfoLoading = ref(false)

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    userInfoLoading.value = true
    userInfo.value = await userStore.getUserInfo()
  } catch (error) {
    console.error('获取用户信息失败:', error)
    showToast('获取用户信息失败', 'error')
  } finally {
    userInfoLoading.value = false
  }
}

// 在组件挂载时获取用户信息
onMounted(() => {
  fetchUserInfo()
})


// 表单验证
const validateForm = () => {
  if (!form.value.old_password) {
    showToast('请输入当前密码', 'error')
    return false
  }
  if (!form.value.new_password) {
    showToast('请输入新密码', 'error')
    return false
  }
  if (!form.value.confirm_password) {
    showToast('请确认新密码', 'error')
    return false
  }
  if (form.value.new_password !== form.value.confirm_password) {
    showToast('两次输入的密码不一致', 'error')
    return false
  }
  if (form.value.new_password.length < 6) {
    showToast('密码长度不能少于6位', 'error')
    return false
  }
  return true
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.modal-content {
  position: relative;
  width: 91.666667%;
  max-width: 28rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-header {
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
}

.modal-header h3 {
  margin: 0;
  color: #111827;
  font-size: 1.125rem;
  font-weight: 500;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
  border-bottom-left-radius: 0.5rem;
  border-bottom-right-radius: 0.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: #111827;
  background-color: white;
  transition: border-color 0.15s ease-in-out;
}

.form-group input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 1px #6366f1;
}

.form-group input:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}

.code-input {
  display: flex;
  gap: 0.75rem;
}

.code-input input {
  flex: 1;
}

.code-btn {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: white;
  background-color: #6366f1;
  border-radius: 0.375rem;
  transition: background-color 0.15s ease-in-out;
}

.code-btn:not(:disabled):hover {
  background-color: #4f46e5;
}

.code-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.375rem;
  transition: all 0.15s ease-in-out;
}

.btn-default {
  color: #374151;
  background-color: white;
  border: 1px solid #d1d5db;
}

.btn-default:not(:disabled):hover {
  background-color: #f9fafb;
}

.btn-primary {
  color: white;
  background-color: #6366f1;
  border: 1px solid transparent;
}

.btn-primary:not(:disabled):hover {
  background-color: #4f46e5;
}

.btn-danger {
  color: white;
  background-color: #ef4444;
  border: 1px solid transparent;
}

.btn-danger:not(:disabled):hover {
  background-color: #dc2626;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 关闭按钮样式 */
.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.25rem;
  color: #6b7280;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: color 0.15s ease-in-out;
}

.close-btn:hover {
  color: #374151;
}

/* 注销弹窗特殊样式 */
.bg-red-50 {
  background-color: #fef2f2;
}

.border-red-100 {
  border-color: #fee2e2;
}

.text-red-400 {
  color: #f87171;
}

.text-red-600 {
  color: #dc2626;
}

.text-red-700 {
  color: #b91c1c;
}

.text-red-800 {
  color: #991b1b;
}

/* 注销弹窗的输入框特殊样式 */
.form-group input.border-red-300 {
  border-color: #fca5a5;
}

.form-group input.focus\:border-red-500:focus {
  border-color: #ef4444;
}

.form-group input.focus\:ring-red-500:focus {
  box-shadow: 0 0 0 1px #ef4444;
}

.input-tips {
  background-color: #f9fafb;
  border-radius: 0.5rem;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
}

.input-tips ul li {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.input-tips ul li span:first-child {
  min-width: 1rem;
  background-color: white;
}

.form-group input.error {
  border-color: #ef4444;
}

.form-group input.error:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 1px #ef4444;
}
</style>