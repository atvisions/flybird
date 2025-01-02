<template>
  <div class="max-w-4xl mx-auto">
    <div class="space-y-6">
      <!-- 账户信息 -->
      <section class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-6 py-4 bg-gray-100 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">账户信息</h2>
        </div>
        
        <div class="p-6 space-y-6">
          <!-- UID -->
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-medium text-gray-500">用户 ID</span>
              <span class="text-sm text-gray-900">{{ uid }}</span>
            </div>
            <div class="text-xs text-gray-500">用户唯一标识</div>
          </div>

          <!-- 昵称 -->
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-medium text-gray-500">昵称</span>
              <span class="text-sm text-gray-900">{{ username }}</span>
              <span class="text-xs text-gray-400" v-if="!username">
                (默认为 Flybird + 手机号后4位)
              </span>
            </div>
            <button 
              @click="openNicknameModal"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-indigo-600 border border-indigo-600 
              hover:bg-indigo-50 transition-colors rounded-md">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              设置
            </button>
          </div>
        </div>
      </section>

      <!-- 账户安全 -->
      <section class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-6 py-4 bg-gray-100 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">账户安全</h2>
        </div>
        
        <div class="p-6 space-y-6">
          <!-- 手机号 -->
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
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
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-red-600 border border-red-600 
              hover:bg-red-50 transition-colors rounded-md">
              注销账户
            </button>
          </div>
        </div>
      </section>

      <!-- Teleport 部分重写所有弹窗 -->
      <Teleport to="body">
        <!-- 昵称设置弹窗 -->
        <div v-if="showNicknameModal" class="modal-overlay">
          <div class="modal-content">
            <div class="modal-header">
              <h3>修改昵称</h3>
              <button class="close-btn" @click="closeNicknameModal">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="form-group">
                <input 
                  type="text"
                  v-model="nickname.state.value"
                  placeholder="请输入新昵称"
                  :disabled="nickname.state.loading"
                  @input="validateNickname"
                  :class="{ 'error': nickname.state.error }"
                />
                <!-- 错误提示 -->
                <div v-if="nickname.state.error" class="text-red-500 text-sm mt-1">
                  {{ nickname.state.error }}
                </div>
                <!-- 简单的提示文字 -->
                <div class="text-gray-400 text-xs mt-1">
                  昵称长度4-8个字符，可使用中文、英文字母、数字
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closeNicknameModal"
                :disabled="nickname.state.loading"
              >
                取消
              </button>
              <button 
                class="btn btn-primary" 
                @click="handleNicknameUpdate"
                :disabled="nickname.state.loading"
              >
                {{ nickname.state.loading ? '更新中...' : '确认' }}
              </button>
            </div>
          </div>
        </div>

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
                    @click="phoneManager.handleSendCode"
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
                />
              </div>
              <div class="form-group">
                <input 
                  type="password" 
                  v-model="password.state.confirmPassword"
                  placeholder="请确认新密码"
                  :disabled="password.state.loading"
                />
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
                <h3 class="text-red-700">账户注销</h3>
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
                  v-model="deleteAccount.state.password"
                  placeholder="请输入登录密码确认"
                  :disabled="deleteAccount.state.loading"
                  class="border-red-300 focus:border-red-500 focus:ring-red-500"
                />
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closeDeleteConfirm"
                :disabled="deleteAccount.state.loading"
              >
                取消
              </button>
              <button 
                class="btn btn-danger" 
                @click="deleteAccount.handleDelete"
                :disabled="deleteAccount.state.loading"
              >
                {{ deleteAccount.state.loading ? '处理中...' : '确认注销' }}
              </button>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { showToast } from '@/components/ToastMessage'
import { useDeleteAccount } from '@/composables/useDeleteAccount'
import { useNickname } from '@/composables/useNickname'
import { usePhone } from '@/composables/usePhone'
import { useChangePassword } from '@/composables/useChangePassword'

const store = useStore()
const router = useRouter()
// 基础信息
const username = computed(() => store.state.userInfo?.data?.user?.username || '未设置')
const uid = computed(() => store.state.userInfo?.data?.user?.uid || '暂无')
const phone = computed(() => store.state.userInfo?.data?.user?.phone || '')

// 使用 composables
const nickname = useNickname()
const phoneManager = usePhone()
const deleteAccount = useDeleteAccount()
const password = useChangePassword()

// 工具方法
const maskPhone = (phone) => {
  if (!phone) return '未绑定'
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

// 弹窗状态
const showNicknameModal = ref(false)
const showPhoneModal = ref(false)
const showPasswordModal = ref(false)
const showDeleteConfirm = ref(false)

// 打开弹窗的方法
const openNicknameModal = () => {
  nickname.value = store.state.userInfo?.username || ''
  showNicknameModal.value = true
}

const openPhoneModal = () => {
  phoneManager.state.value = ''
  phoneManager.state.code = ''
  showPhoneModal.value = true
}

const openPasswordModal = () => {
  showPasswordModal.value = true
}

const openDeleteConfirm = () => {
  deleteAccount.state.password = ''
  showDeleteConfirm.value = true
}

// 关闭弹窗的方法
const closeNicknameModal = () => {
  showNicknameModal.value = false
  nickname.value = ''
}

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
  deleteAccount.state.password = ''
}

// 处理成功回调
const handlePasswordSuccess = () => {
  closePasswordModal()
  showToast('密码修改成功', 'success')
}

// 处理昵称更新
const handleNicknameUpdate = async () => {
  const success = await nickname.handleUpdate()
  if (success) {
    closeNicknameModal()
  }
}

// 处理密码更新
const handlePasswordUpdate = async () => {
  const success = await password.handleUpdate()
  if (success) {
    closePasswordModal()
    showToast('密码修改成功', 'success')
  }
}

// 处理手机号更新
const handlePhoneUpdate = async () => {
  const success = await phoneManager.handleUpdate()
  if (success) {
    closePhoneModal()
  }
}

// 实时验证昵称
const validateNickname = () => {
  nickname.state.error = nickname.validateNickname(nickname.state.value)
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