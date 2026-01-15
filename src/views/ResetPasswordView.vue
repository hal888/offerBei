<template>
  <div class="reset-container">
    <div class="reset-card">
      <h1 class="reset-title">{{ t('auth.forgot.resetTitle') }}</h1>
      <p class="reset-subtitle">{{ t('auth.forgot.resetSubtitle') }}</p>
      <p class="reset-description">{{ t('auth.forgot.resetDesc') }}</p>
      
      <div class="reset-form">
        <!-- 新密码输入框 -->
        <div class="form-group">
          <label for="newPassword" class="form-label">{{ t('auth.forgot.newPasswordLabel') }}</label>
          <input 
            type="password" 
            id="newPassword" 
            v-model="newPassword" 
            class="form-input" 
            :placeholder="t('auth.forgot.newPasswordPlaceholder')" 
            required
            @input="checkPasswordStrength"
          />
          <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
          <!-- 密码强度提示 -->
          <div class="password-strength" v-if="newPassword.trim()">
            <div 
              class="strength-bar" 
              :class="passwordStrengthClass"
              :style="{ width: passwordStrengthWidth }"
            ></div>
            <div class="strength-text">{{ passwordStrengthText }}</div>
          </div>
        </div>
        
        <!-- 确认密码输入框 -->
        <div class="form-group">
          <label for="confirmPassword" class="form-label">{{ t('auth.forgot.confirmPasswordLabel') }}</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            class="form-input" 
            :placeholder="t('auth.forgot.confirmPasswordPlaceholder')"
            required
            @input="checkPasswordMatch"
          />
          <div v-if="confirmError" class="error-message">{{ confirmError }}</div>
        </div>
        
        <!-- 重置按钮 -->
        <button 
          class="reset-button" 
          @click="handleResetPassword"
          :disabled="isLoading || !isFormValid"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? t('auth.forgot.resetting') : t('auth.forgot.resetBtn') }}
        </button>
        
        <!-- 返回登录链接 -->
        <div class="reset-footer">
          <p>{{ t('auth.forgot.successReset') }}<button class="login-link" @click="handleLogin">{{ t('auth.forgot.loginLink') }}</button></p>
        </div>
      </div>
    </div>
    
    <!-- 错误提示组件 -->
    <ErrorMessage 
      :show="showError" 
      :message="errorMessage" 
      :title="errorTitle"
      @close="closeError"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import apiClient from '@/utils/api.js'
import ErrorMessage from '@/components/ErrorMessage.vue'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const newPassword = ref('')
const confirmPassword = ref('')
const isLoading = ref(false)

// 错误信息
const passwordError = ref('')
const confirmError = ref('')

// 密码强度相关
const passwordStrength = ref(0)
const passwordStrengthText = ref('')
const passwordStrengthClass = ref('')
const passwordStrengthWidth = ref('0%')

// 错误提示相关
const showError = ref(false)
const errorMessage = ref('')
const errorTitle = ref('提示')
// 错误提示关闭后的回调函数
const errorCloseCallback = ref(null)

// 从URL中获取参数
const token = ref('')
const email = ref('')

onMounted(() => {
  // 从URL查询参数中获取token和email
  token.value = route.query.token || ''
  email.value = route.query.email || ''
  
  // 如果没有token或email，显示错误信息，用户点击确定后跳转到登录页面
  if (!token.value || !email.value) {
    showErrorMessage(t('auth.forgot.error.invalidLink'), t('auth.login.error.failed'), () => {
      router.push('/login')
    })
  }
})

// 显示错误信息
const showErrorMessage = (message, title = '提示', callback = null) => {
  errorMessage.value = message
  errorTitle.value = title
  errorCloseCallback.value = callback
  showError.value = true
}

// 关闭错误信息
const closeError = () => {
  showError.value = false
  errorMessage.value = ''
  errorTitle.value = '提示'
  // 执行回调函数
  if (errorCloseCallback.value) {
    const callback = errorCloseCallback.value
    errorCloseCallback.value = null
    callback()
  }
}

// 检查密码强度
const checkPasswordStrength = () => {
  const passwordValue = newPassword.value
  if (!passwordValue.trim()) {
    passwordError.value = t('auth.register.error.passwordRequired')
    passwordStrength.value = 0
  } else {
    // 密码强度规则：至少8位，包含大小写字母、数字和特殊符号
    let strength = 0
    
    // 长度检查
    if (passwordValue.length >= 8) strength += 1
    
    // 包含小写字母
    if (/[a-z]/.test(passwordValue)) strength += 1
    
    // 包含大写字母
    if (/[A-Z]/.test(passwordValue)) strength += 1
    
    // 包含数字
    if (/\d/.test(passwordValue)) strength += 1
    
    // 包含特殊符号
    if (/[^a-zA-Z0-9]/.test(passwordValue)) strength += 1
    
    passwordStrength.value = strength
    
    // 更新密码强度文本和样式
    switch (strength) {
      case 0:
      case 1:
        passwordStrengthText.value = t('auth.register.passwordStrength.weak')
        passwordStrengthClass.value = 'weak'
        passwordStrengthWidth.value = '20%'
        passwordError.value = t('auth.register.passwordStrength.msg.tooWeak')
        break
      case 2:
        passwordStrengthText.value = t('auth.register.passwordStrength.medium')
        passwordStrengthClass.value = 'medium'
        passwordStrengthWidth.value = '40%'
        passwordError.value = t('auth.register.passwordStrength.msg.general')
        break
      case 3:
        passwordStrengthText.value = t('auth.register.passwordStrength.strong')
        passwordStrengthClass.value = 'strong'
        passwordStrengthWidth.value = '60%'
        passwordError.value = ''
        break
      case 4:
        passwordStrengthText.value = t('auth.register.passwordStrength.veryStrong')
        passwordStrengthClass.value = 'very-strong'
        passwordStrengthWidth.value = '80%'
        passwordError.value = ''
        break
      case 5:
        passwordStrengthText.value = t('auth.register.passwordStrength.extremelyStrong')
        passwordStrengthClass.value = 'extremely-strong'
        passwordStrengthWidth.value = '100%'
        passwordError.value = ''
        break
    }
  }
}

// 检查密码是否匹配
const checkPasswordMatch = () => {
  if (!confirmPassword.value.trim()) {
    confirmError.value = t('auth.forgot.error.confirm')
    return
  }
  
  if (confirmPassword.value !== newPassword.value) {
    confirmError.value = t('auth.forgot.error.mismatch')
  } else {
    confirmError.value = ''
  }
}

// 表单验证
const isFormValid = computed(() => {
  return (
    newPassword.value.trim() &&
    confirmPassword.value.trim() &&
    !passwordError.value &&
    !confirmError.value &&
    newPassword.value === confirmPassword.value &&
    passwordStrength.value >= 3
  )
})

// 处理密码重置
const handleResetPassword = async () => {
  if (!isFormValid.value) {
    showErrorMessage(t('auth.forgot.error.invalid'), t('auth.login.error.failed'))
    return
  }
  
  try {
    isLoading.value = true
    // 调用密码重置API
    await apiClient.post('/auth/reset-password', {
      email: email.value,
      token: token.value,
      newPassword: newPassword.value
    })
    
    // 重置成功，显示提示信息，用户点击确定后跳转到登录页面
    showErrorMessage(t('auth.forgot.successReset'), '重置成功', () => {
      router.push('/login')
    })
  } catch (error) {
    console.error('重置密码失败:', error)
    if (error.response?.data?.error) {
      showErrorMessage(error.response.data.error, t('auth.login.error.failed'))
    } else {
      showErrorMessage(t('auth.forgot.error.invalidLink'), t('auth.login.error.failed'))
    }
  } finally {
    isLoading.value = false
  }
}

// 返回登录页面
const handleLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.reset-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.reset-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 450px;
  animation: fadeInUp 0.6s ease-out;
}

.reset-title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  text-align: center;
  margin-bottom: 8px;
}

.reset-subtitle {
  font-size: 18px;
  color: #333;
  text-align: center;
  margin-bottom: 8px;
}

.reset-description {
  font-size: 14px;
  color: #666;
  text-align: center;
  margin-bottom: 32px;
}

.reset-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  width: 100%;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error-message {
  font-size: 12px;
  color: #e74c3c;
  margin-top: 4px;
}

/* 密码强度样式 */
.password-strength {
  margin-top: 8px;
}

.strength-bar {
  height: 4px;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-bar.weak {
  background: #e74c3c;
}

.strength-bar.medium {
  background: #f39c12;
}

.strength-bar.strong {
  background: #2ecc71;
}

.strength-bar.very-strong {
  background: #27ae60;
}

.strength-bar.extremely-strong {
  background: #16a085;
}

.strength-text {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  text-align: right;
}

.reset-button {
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.reset-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.reset-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.reset-footer {
  text-align: center;
  font-size: 14px;
  color: #666;
  margin-top: 16px;
}

.login-link {
  background: none;
  border: none;
  color: #667eea;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-left: 4px;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #5a6fd8;
  text-decoration: underline;
}

/* 加载动画 */
.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>