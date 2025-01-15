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
            <div class="flex space-x-2">
              <button 
                v-if="email"
                @click="handleUnbindEmail"
                class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-red-600 border border-red-600 
                hover:bg-red-50 transition-colors rounded-md">
                取消绑定
              </button>
              <button 
                @click="openEmailModal"
                class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-indigo-600 border border-indigo-600 
                hover:bg-indigo-50 transition-colors rounded-md">
                {{ email ? '更换邮箱' : '绑定邮箱' }}
              </button>
            </div>
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
                  v-model.trim="phoneManager.state.value"
                  placeholder="请输入新手机号"
                  :disabled="phoneManager.state.loading"
                />
              </div>
              <div class="form-group">
                <div class="code-input">
                  <input 
                    type="text" 
                    v-model.trim="phoneManager.state.code"
                    maxlength="6"
                    placeholder="请输入验证码"
                    :disabled="phoneManager.state.loading"
                    @input="e => phoneManager.state.code = e.target.value.replace(/\D/g, '').slice(0, 6)"
                  />
                  <button 
                    @click="handlePhoneSendCode"
                    :disabled="isPhoneCodeButtonDisabled"
                    class="code-btn"
                  >
                    {{ phoneManager.state.countdown > 0 
                      ? `${phoneManager.state.countdown}s` 
                      : (phoneManager.state.loading ? '发送中...' : '获取验证码') 
                    }}
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
                :disabled="!isPhoneFormValid || phoneManager.state.loading"
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
              <!-- 原密码 -->
              <div class="form-group">
                <div class="relative">
                  <input 
                    :type="showOldPassword ? 'text' : 'password'"
                    v-model="passwordFormState.oldPassword"
                    placeholder="请输入当前密码"
                  />
                  <button 
                    type="button"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center"
                    @click="showOldPassword = !showOldPassword"
                  >
                    <svg 
                      class="h-5 w-5 text-gray-400" 
                      :class="{ 'text-indigo-600': showOldPassword }"
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path 
                        v-if="showOldPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2" 
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path 
                        v-if="showOldPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                      <path
                        v-else
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                      />
                    </svg>
                  </button>
                </div>
              </div>
              
              <!-- 新密码 -->
              <div class="form-group">
                <div class="relative">
                  <input 
                    :type="showNewPassword ? 'text' : 'password'"
                    v-model="passwordFormState.newPassword"
                    @input="handlePasswordInput"
                    placeholder="请输入新密码"
                  />
                  <button 
                    type="button"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center"
                    @click="showNewPassword = !showNewPassword"
                  >
                    <svg 
                      class="h-5 w-5 text-gray-400" 
                      :class="{ 'text-indigo-600': showNewPassword }"
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path 
                        v-if="showNewPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2" 
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path 
                        v-if="showNewPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                      <path
                        v-else
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                      />
                    </svg>
                  </button>
                </div>
                <!-- 密码强度指示器 -->
                <div class="password-strength">
                  <div class="strength-text" :class="strengthTextClass">
                    密码强度: {{ strengthText }}
                  </div>
                  <div class="strength-bar">
                    <div 
                      class="strength-progress" 
                      :class="strengthColorClass"
                      :style="{ width: (passwordFormState.strength * 16.67) + '%' }"
                    ></div>
                  </div>
                </div>
                <!-- 密码格式要求提示 -->
                <div class="password-requirements text-sm text-gray-500 mt-2">
                  <p>密码必须满足：</p>
                  <ul class="list-disc pl-5 space-y-1">
                    <li>长度至少8位</li>
                    <li>包含字母</li>
                    <li>包含数字</li>
                  </ul>
                  <p class="mt-1">建议包含：</p>
                  <ul class="list-disc pl-5 space-y-1">
                    <li>大写字母</li>
                    <li>特殊字符（!@#$%^&*）</li>
                  </ul>
                </div>
              </div>

              <!-- 确认密码 -->
              <div class="form-group">
                <div class="relative">
                  <input 
                    :type="showConfirmPassword ? 'text' : 'password'"
                    v-model="passwordFormState.confirmPassword"
                    placeholder="请确认新密码"
                  />
                  <button 
                    type="button"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center"
                    @click="showConfirmPassword = !showConfirmPassword"
                  >
                    <svg 
                      class="h-5 w-5 text-gray-400" 
                      :class="{ 'text-indigo-600': showConfirmPassword }"
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path 
                        v-if="showConfirmPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2" 
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path 
                        v-if="showConfirmPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                      <path
                        v-else
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closePasswordModal"
                :disabled="passwordFormState.loading"
              >
                取消
              </button>
              <button 
                class="btn btn-primary" 
                @click="handlePasswordUpdate"
                :disabled="!isPasswordFormValid"
              >
                {{ passwordFormState.loading ? '修改中...' : '确认' }}
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
                <div class="relative">
                  <input 
                    :type="showPassword ? 'text' : 'password'"
                    v-model="deleteFormState.password"
                    placeholder="请输入登录密码确认"
                    :disabled="deleteFormState.loading"
                    class="border-red-300 focus:border-red-500 focus:ring-red-500"
                  />
                  <button 
                    type="button"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center"
                    @click="showPassword = !showPassword"
                  >
                    <svg 
                      class="h-5 w-5 text-gray-400" 
                      :class="{ 'text-red-600': showPassword }"
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path 
                        v-if="showPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2" 
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path 
                        v-if="showPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                      <path
                        v-else
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closeDeleteConfirm"
                :disabled="deleteFormState.loading"
              >
                取消
              </button>
              <button 
              class="btn btn-danger" 
              @click="handleConfirmDelete"
              :disabled="deleteFormState.loading || !deleteFormState.password"
            >
              {{ deleteFormState.loading ? '注销中...' : '确认注销' }}
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
                <div class="relative">
                  <input 
                    :type="showPassword ? 'text' : 'password'"
                    v-model="emailManager.state.password"
                    placeholder="请输入登录密码"
                    :disabled="emailManager.state.loading"
                  />
                  <button 
                    type="button"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center"
                    @click="showPassword = !showPassword"
                  >
                    <svg 
                      class="h-5 w-5 text-gray-400" 
                      :class="{ 'text-indigo-600': showPassword }"
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path 
                        v-if="showPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2" 
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path 
                        v-if="showPassword"
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                      <path
                        v-else
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2"
                        d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                      />
                    </svg>
                  </button>
                </div>
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
                    :disabled="isEmailCodeButtonDisabled"
                    class="code-btn"
                  >
                    {{ emailManager.state.countdown > 0 
                      ? `${emailManager.state.countdown}s` 
                      : (emailManager.state.loading ? '发送中...' : '获取验证码') 
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
                :disabled="!isEmailFormValid || emailManager.state.loading"
              >
                {{ emailManager.state.loading ? (email ? '更换中...' : '绑定中...') : '确认' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 邮箱解绑确认弹窗 -->
        <div v-if="showUnbindEmailModal" class="modal-overlay">
          <div class="modal-content">
            <div class="modal-header">
              <div class="flex items-center space-x-2">
                <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <h3 class="text-gray-900">取消邮箱绑定</h3>
              </div>
              <button class="close-btn" @click="closeUnbindEmailModal">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="bg-gray-50 p-4 rounded-md mb-4 border border-gray-200">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div class="ml-3">
                    <h3 class="text-sm font-medium text-gray-900">
                      请确认以下信息
                    </h3>
                    <div class="mt-2 text-sm text-gray-600">
                      <ul class="list-disc pl-5 space-y-1">
                        <li>取消绑定后将无法接收邮件通知</li>
                        <li>需要输入登录密码确认操作</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <input 
                  type="password" 
                  v-model="unbindEmailForm.password"
                  placeholder="请输入登录密码确认"
                  :disabled="unbindEmailLoading"
                  class="border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closeUnbindEmailModal"
                :disabled="unbindEmailLoading"
              >
                取消
              </button>
              <button 
                class="btn btn-primary" 
                @click="confirmUnbindEmail"
                :disabled="unbindEmailLoading || !unbindEmailForm.password"
              >
                {{ unbindEmailLoading ? '处理中...' : '确认解绑' }}
              </button>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from '@/components/ToastMessage'
import { useDeleteAccount } from '@/composables/useDeleteAccount'
import { usePhone } from '@/composables/usePhone'
import { useEmail } from '@/composables/useEmail'
import { useChangePassword } from '@/composables/useChangePassword'
import { account } from '@/api/account'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { useAccountStore } from '@/stores/account'

const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()
const accountStore = useAccountStore()

// 手机号掩码处理函数
const maskPhone = (phone) => {
  if (!phone) return '未绑定'
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

// 从 accountStore 获取用户信息
const phone = computed(() => accountStore.userInfo?.phone)
const email = computed(() => accountStore.userInfo?.email)

// 弹窗状态
const showEmailModal = ref(false)
const showUnbindEmailModal = ref(false)
const showPhoneModal = ref(false)
const showPasswordModal = ref(false)
const showDeleteConfirm = ref(false)
const showPassword = ref(false)

// 密码状态
const passwordFormState = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
  loading: false,
  strength: 0
})

// 邮箱解绑相关状态
const unbindEmailLoading = ref(false)
const unbindEmailForm = ref({
  password: ''
})

// 邮箱解绑相关方法
const closeUnbindEmailModal = () => {
  showUnbindEmailModal.value = false
  unbindEmailForm.value.password = ''
}

const handleUnbindEmail = () => {
  showUnbindEmailModal.value = true
}

const confirmUnbindEmail = async () => {
  try {
    unbindEmailLoading.value = true
    const response = await account.unbindEmail({
      password: unbindEmailForm.value.password
    })
    
    if (response?.data?.message) {
      closeUnbindEmailModal()
      await accountStore.fetchUserInfo()
      showToast(response.data.message || '邮箱解绑成功', 'success')
    }
  } catch (error) {
    console.error('邮箱解绑失败:', error)
    const errorMsg = error.response?.data?.detail || 
                    error.response?.data?.message || 
                    error.message || 
                    '邮箱解绑失败'
    showToast(errorMsg, 'error')
  } finally {
    unbindEmailLoading.value = false
  }
}

// 密码显示状态
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// 打开密码修改弹窗时重置所有状态
const openPasswordModal = () => {
  // 重置表单状态
  passwordFormState.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
    loading: false,
    strength: 0
  }
  // 重置密码显示状态
  showOldPassword.value = false
  showNewPassword.value = false
  showConfirmPassword.value = false
  showPasswordModal.value = true
  console.log('Password modal opened:', showPasswordModal.value)
}

// 关闭密码修改弹窗时重置所有状态
const closePasswordModal = () => {
  showPasswordModal.value = false
  // 重置表单状态
  passwordFormState.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
    loading: false,
    strength: 0
  }
  // 重置密码显示状态
  showOldPassword.value = false
  showNewPassword.value = false
  showConfirmPassword.value = false
}

// 邮箱管理器
const emailManager = useEmail()
const phoneManager = usePhone()
const { validatePassword } = useChangePassword()
const { loading } = useDeleteAccount()

// 修改密码强度更新的处理方法
const handlePasswordInput = () => {
  const strength = validatePassword(passwordFormState.value.newPassword)
  console.log('Password strength updated:', strength)
  passwordFormState.value.strength = strength
}

// 密码表单验证
const isPasswordFormValid = computed(() => {
  // 添加调试日志
  console.log('Password validation:', {
    oldPassword: !!passwordFormState.value.oldPassword,
    newPassword: !!passwordFormState.value.newPassword,
    confirmPassword: !!passwordFormState.value.confirmPassword,
    passwordsMatch: passwordFormState.value.newPassword === passwordFormState.value.confirmPassword,
    strength: passwordFormState.value.strength,
    loading: passwordFormState.value.loading
  })

  return passwordFormState.value.oldPassword && 
         passwordFormState.value.newPassword && 
         passwordFormState.value.confirmPassword && 
         passwordFormState.value.newPassword === passwordFormState.value.confirmPassword &&
         passwordFormState.value.strength >= 3 &&
         !passwordFormState.value.loading
})

// 处理密码更新
const handlePasswordUpdate = async () => {
  try {
    passwordFormState.value.loading = true
    const response = await account.updatePassword({
      oldPassword: passwordFormState.value.oldPassword,
      newPassword: passwordFormState.value.newPassword,
      confirmPassword: passwordFormState.value.confirmPassword
    })
    
    if (response?.data?.message) {
      closePasswordModal()
      showToast(response.data.message || '密码修改成功', 'success')
    }
  } catch (error) {
    console.error('密码修改失败:', error)
    console.log('Error response:', error.response)
    console.log('Form data:', passwordFormState.value)
    
    const errorMsg = error.response?.data?.detail || 
                    error.response?.data?.message || 
                    error.message || 
                    '密码修改失败'
    showToast(errorMsg, 'error')
  } finally {
    passwordFormState.value.loading = false
  }
}

// 密码强度相关
const strengthText = computed(() => {
  const strength = passwordFormState.value.strength
  if (strength <= 2) return '弱'
  if (strength <= 3) return '中'
  return '强'
})

const strengthTextClass = computed(() => {
  const strength = passwordFormState.value.strength
  if (strength <= 2) return 'text-red-500'
  if (strength <= 3) return 'text-yellow-500'
  return 'text-green-500'
})

const strengthColorClass = computed(() => {
  const strength = passwordFormState.value.strength
  if (strength <= 2) return 'bg-red-500'
  if (strength <= 3) return 'bg-yellow-500'
  return 'bg-green-500'
})

// 监听密码修改弹窗状态
onMounted(() => {
  watch(showPasswordModal, (newVal) => {
    console.log('Password modal state changed:', newVal)
  })
})

// 用户信息
const userInfo = ref(null)

// 用户信息加载状态
const userInfoLoading = ref(false)

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    userInfoLoading.value = true
    await accountStore.fetchUserInfo()
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
  watch(showPasswordModal, (newVal) => {
    console.log('Password modal state changed:', newVal)
  })
})

// 监听 accountStore 中的用户信息变化
watch(
  [() => accountStore.userInfo, () => authStore.isLoggedIn],
  ([newUserInfo, isLoggedIn]) => {
    if (newUserInfo && isLoggedIn) {
      userInfo.value = {
        ...newUserInfo
      }
    } else {
      userInfo.value = null
    }
  },
  { immediate: true, deep: true }
)

// 手机号管理相关方法
const openPhoneModal = () => {
  phoneManager.state.value = ''
  phoneManager.state.code = ''
  phoneManager.state.loading = false
  phoneManager.state.countdown = 0
  showPhoneModal.value = true
  console.log('Phone modal opened:', showPhoneModal.value) // 添加调试日志
}

const closePhoneModal = () => {
  showPhoneModal.value = false
  phoneManager.state.value = ''
  phoneManager.state.code = ''
  phoneManager.state.loading = false
  phoneManager.state.countdown = 0
}

// 手机号验证码按钮禁用状态
const isPhoneCodeButtonDisabled = computed(() => {
  const phoneRegex = /^1[3-9]\d{9}$/
  return phoneManager.state.loading || 
         phoneManager.state.countdown > 0 || 
         !phoneManager.state.value ||
         !phoneRegex.test(phoneManager.state.value)
})

// 手机号表单验证
const isPhoneFormValid = computed(() => {
  const phoneRegex = /^1[3-9]\d{9}$/
  const isValidPhone = phoneRegex.test(phoneManager.state.value)
  const isValidCode = phoneManager.state.code?.length === 6

  return phoneManager.state.value && 
         phoneManager.state.code && 
         isValidPhone && 
         isValidCode && 
         !phoneManager.state.loading
})

// 发送手机验证码
const handlePhoneSendCode = async () => {
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneManager.state.value) {
    showToast('请输入新手机号', 'warning')
    return
  }
  
  if (!phoneRegex.test(phoneManager.state.value)) {
    showToast('请输入正确的手机号格式', 'warning')
    return
  }
  
  try {
    phoneManager.state.loading = true
    const response = await account.sendVerifyCode({
      phone: phoneManager.state.value.trim(),
      scene: 'change_phone'  // 指定场景为更换手机号
    })
    
    if (response?.data?.code === 200) {
      showToast(response.data.message || '验证码已发送', 'success')
      phoneManager.state.countdown = 60
      startPhoneCountdown()
    }
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 
                    error.response?.data?.message || 
                    error.message || 
                    '发送验证码失败'
    showToast(errorMsg, 'error')
  } finally {
    phoneManager.state.loading = false
  }
}

// 更新手机号
const handlePhoneUpdate = async () => {
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneManager.state.value || !phoneRegex.test(phoneManager.state.value)) {
    showToast('请输入正确的手机号', 'warning')
    return
  }
  
  if (!phoneManager.state.code || phoneManager.state.code.length !== 6) {
    showToast('请输入6位验证码', 'warning')
    return
  }

  try {
    phoneManager.state.loading = true
    const response = await account.changePhone({
      phone: phoneManager.state.value.trim(),
      code: phoneManager.state.code.trim()
    })

    if (response?.data?.code === 200 || response?.status === 200) {
      showToast(response.data?.message || '手机号修改成功', 'success')
      closePhoneModal()
      await accountStore.fetchUserInfo()
    }
  } catch (error) {
    console.error('手机号更新失败:', error)
    let errorMsg = '手机号更新失败'
    
    if (error.response?.data) {
      const errorData = error.response.data
      if (typeof errorData.detail === 'object') {
        errorMsg = Object.values(errorData.detail)[0]
      } else if (typeof errorData.detail === 'string') {
        errorMsg = errorData.detail
      } else if (errorData.message) {
        errorMsg = errorData.message
      }
    }
    
    showToast(errorMsg, 'error')
  } finally {
    phoneManager.state.loading = false
  }
}

// 倒计时管理
let phoneTimer = null

const startPhoneCountdown = () => {
  if (phoneTimer) {
    clearInterval(phoneTimer)
  }
  phoneManager.state.countdown = 60
  phoneTimer = setInterval(() => {
    if (phoneManager.state.countdown > 0) {
      phoneManager.state.countdown--
    } else {
      clearInterval(phoneTimer)
      phoneTimer = null
    }
  }, 1000)
}

// 在组件卸载时清理定时器
onUnmounted(() => {
  if (phoneTimer) {
    clearInterval(phoneTimer)
    phoneTimer = null
  }
})

// 邮箱相关方法
const openEmailModal = () => {
  emailManager.state.value = ''
  emailManager.state.code = ''
  emailManager.state.password = ''
  showPassword.value = false
  showEmailModal.value = true
}

const closeEmailModal = () => {
  showEmailModal.value = false
  emailManager.state.value = ''
  emailManager.state.code = ''
  emailManager.state.password = ''
  emailManager.state.loading = false
  showPassword.value = false
}

// 邮箱验证码按钮禁用状态
const isEmailCodeButtonDisabled = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailManager.state.loading || 
         emailManager.state.countdown > 0 || 
         !emailManager.state.value ||
         !emailRegex.test(emailManager.state.value) ||
         !emailManager.state.password
})

// 邮箱表单验证
const isEmailFormValid = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  const isValidEmail = emailRegex.test(emailManager.state.value)

  return emailManager.state.value && 
         emailManager.state.code && 
         emailManager.state.password &&
         isValidEmail && 
         emailManager.state.code.length === 6
})

// 发送邮箱验证码
const handleEmailSendCode = async () => {
  if (!emailManager.state.value) {
    showToast('请输入邮箱地址', 'warning')
    return
  }
  
  if (!emailManager.state.password) {
    showToast('请输入登录密码', 'warning')
    return
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(emailManager.state.value)) {
    showToast('请输入正确的邮箱格式', 'warning')
    return
  }
  
  try {
    emailManager.state.loading = true
    const response = await account.sendEmailCode({
      email: emailManager.state.value,
      password: emailManager.state.password
    })
    
    if (response?.data?.message) {
      showToast(response.data.message, 'success')
      emailManager.state.countdown = 60
      startEmailCountdown()
    }
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 
                    error.message || 
                    '发送验证码失败'
    showToast(errorMsg, 'error')
  } finally {
    emailManager.state.loading = false
  }
}

// 处理邮箱更新
const handleEmailUpdate = async () => {
  if (!isEmailFormValid.value) {
    showToast('请填写完整信息', 'warning')
    return
  }

  try {
    emailManager.state.loading = true
    const response = await account.bindEmail({
      email: emailManager.state.value,
      code: emailManager.state.code,
      password: emailManager.state.password
    })

    if (response?.data?.message) {
      showToast(response.data.message, 'success')
      closeEmailModal()
      await accountStore.fetchUserInfo()
    }
  } catch (error) {
    console.error('邮箱更新失败:', error)
    const errorMsg = error.response?.data?.detail || 
                    error.message || 
                    '邮箱更新失败'
    showToast(errorMsg, 'error')
  } finally {
    emailManager.state.loading = false
  }
}

// 邮箱倒计时管理
let emailTimer = null

const startEmailCountdown = () => {
  if (emailTimer) {
    clearInterval(emailTimer)
  }
  emailManager.state.countdown = 60
  emailTimer = setInterval(() => {
    if (emailManager.state.countdown > 0) {
      emailManager.state.countdown--
    } else {
      clearInterval(emailTimer)
      emailTimer = null
    }
  }, 1000)
}

// 在组件卸载时清理定时器
onUnmounted(() => {
  if (emailTimer) {
    clearInterval(emailTimer)
  }
  if (phoneTimer) {
    clearInterval(phoneTimer)
  }
})

// 注销账号相关状态
const deleteFormState = ref({
  password: '',
  loading: false
})

// 注销账号相关方法
const openDeleteConfirm = () => {
  deleteFormState.value.password = ''
  showDeleteConfirm.value = true
}

const closeDeleteConfirm = () => {
  showDeleteConfirm.value = false
  deleteFormState.value.password = ''
}

// 处理确认注销
const handleConfirmDelete = async () => {
  if (!deleteFormState.value.password) {
    showToast('请输入密码', 'warning')
    return
  }
  
  try {
    deleteFormState.value.loading = true
    const response = await account.deleteAccount({
      password: deleteFormState.value.password
    })
    
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
    const errorMsg = error.response?.data?.detail || 
                    error.response?.data?.message || 
                    error.message || 
                    '注销失败'
    showToast(errorMsg, 'error')
  } finally {
    deleteFormState.value.loading = false
  }
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

/* 添加密码强度指示器样式 */
.password-strength {
  margin-top: 0.5rem;
}

.strength-text {
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.strength-bar {
  height: 4px;
  background-color: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.strength-progress {
  height: 100%;
  transition: width 0.3s ease;
}
</style>