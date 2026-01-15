<template>
  <div class="register-container">
    <div class="register-card">
      <h1 class="register-title">{{ t('auth.register.title') }}</h1>
      <p class="register-subtitle">{{ t('auth.register.subtitle') }}</p>
      
      <div class="register-form">
        <!-- 邮箱输入框 -->
        <div class="form-group">
          <label for="email" class="form-label">{{ t('auth.register.emailLabel') }}</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            class="form-input" 
            :placeholder="t('auth.register.emailPlaceholder')" 
            required
            @input="validateEmail; clearEmailError"
          />
          <div v-if="emailError" class="error-message">{{ emailError }}</div>
        </div>
        
        <!-- 验证码输入框和获取按钮 -->
        <div class="form-group code-group">
          <label for="verificationCode" class="form-label">{{ t('auth.register.codeLabel') }}</label>
          <div class="code-input-container">
            <input 
              type="text" 
              id="verificationCode" 
              v-model="verificationCode" 
              class="form-input code-input" 
              :placeholder="t('auth.register.codePlaceholder')" 
              required
              @input="clearCodeError"
            />
            <button 
              class="get-code-button" 
              @click="getVerificationCode"
              :disabled="isGettingCode || emailError || !email.trim()"
            >
              {{ isGettingCode ? `${countdown}s` : t('auth.register.getCode') }}
            </button>
          </div>
          <div v-if="codeError" class="error-message">{{ codeError }}</div>
        </div>
        
        <!-- 密码输入框 -->
        <div class="form-group">
          <label for="password" class="form-label">{{ t('auth.register.passwordLabel') }}</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            class="form-input" 
            :placeholder="t('auth.register.passwordPlaceholder')" 
            required
            @input="checkPasswordStrength"
          />
          <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
          <!-- 密码强度提示 -->
          <div class="password-strength" v-if="password.trim()">
            <div 
              class="strength-bar" 
              :class="passwordStrengthClass"
              :style="{ width: passwordStrengthWidth }"
            ></div>
            <div class="strength-text">{{ passwordStrengthText }}</div>
          </div>
        </div>
        
        <!-- 注册按钮 -->
        <button 
          class="register-button" 
          @click="handleRegister"
          :disabled="isLoading || !isFormValid"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? t('auth.register.registering') : t('auth.register.registerBtn') }}
        </button>
        
        <!-- 登录链接 -->
        <div class="register-footer">
          <p>{{ t('auth.register.hasAccount') }}<button class="login-link" @click="handleLogin">{{ t('auth.register.loginLink') }}</button></p>
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
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import apiClient from '@/utils/api.js'
import ErrorMessage from '@/components/ErrorMessage.vue'
import { trackEvent } from '@/utils/analytics'

const router = useRouter()
const { t, locale } = useI18n()
const email = ref('')
const password = ref('')
const verificationCode = ref('')
const isLoading = ref(false)
const isGettingCode = ref(false)
const countdown = ref(0)
let countdownTimer = null

// 错误信息
const emailError = ref('')
const codeError = ref('')
const passwordError = ref('')

// 错误提示遮盖层
const showError = ref(false)
const errorMessage = ref('')
const errorTitle = ref(t('auth.register.title') || '注册失败')
// 错误提示关闭后的回调函数
const errorCloseCallback = ref(null)

// 密码强度相关
const passwordStrength = ref(0)
const passwordStrengthText = ref('')
const passwordStrengthClass = ref('')
const passwordStrengthWidth = ref('0%')

// 显示错误信息
const showErrorMessage = (message, callback = null) => {
  errorMessage.value = message
  errorCloseCallback.value = callback
  showError.value = true
}

// 关闭错误信息
const closeError = () => {
  showError.value = false
  errorMessage.value = ''
  // 执行回调函数
  if (errorCloseCallback.value) {
    const callback = errorCloseCallback.value
    errorCloseCallback.value = null
    callback()
  }
}

// 清除验证码错误
const clearCodeError = () => {
  codeError.value = ''
}

// 清除邮箱错误
const clearEmailError = () => {
  emailError.value = ''
}

// 邮箱验证
const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email.value.trim()) {
    emailError.value = t('auth.register.error.emailRequired')
    return false
  } else if (!emailRegex.test(email.value)) {
    emailError.value = t('auth.register.error.emailInvalid')
    return false
  } else {
    emailError.value = ''
    return true
  }
}

// 检查密码强度
const checkPasswordStrength = () => {
  const passwordValue = password.value
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

// 表单验证
const isFormValid = computed(() => {
  return (
    email.value.trim() &&
    !emailError.value &&
    verificationCode.value.trim() &&
    !codeError.value &&
    password.value.trim() &&
    !passwordError.value &&
    passwordStrength.value >= 3
  )
})

// 获取验证码
const getVerificationCode = async () => {
  if (!validateEmail()) return
  
  try {
    isGettingCode.value = true
    countdown.value = 60
    
    // 调用后端API发送验证码
    await apiClient.post('/auth/send-verification-code', { 
      email: email.value,
      locale: locale.value
    })
    
    // 开始倒计时
    countdownTimer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(countdownTimer)
        isGettingCode.value = false
      }
    }, 1000)
  } catch (error) {
    console.error('发送验证码失败:', error)
    showErrorMessage(error.response?.data?.error || '发送验证码失败，请重试')
    isGettingCode.value = false
  }
}

// 处理注册
const handleRegister = async () => {
  if (!isFormValid.value) {
    showErrorMessage(t('auth.register.error.incomplete'))
    return
  }
  
  try {
    isLoading.value = true
    // 调用注册API
    const response = await apiClient.post('/auth/register', {
      email: email.value,
      password: password.value,
      verificationCode: verificationCode.value
    })
    
    // Track register event
    trackEvent('register', { method: 'email' })

    // 注册成功，显示提示信息，用户点击确定后跳转到登录页面
    showErrorMessage('注册成功，请登录', () => {
      router.push('/login')
    })
  } catch (error) {
    console.error('注册失败:', error)
    let errorMsg = '注册失败，请重试'
    if (error.response?.data?.error) {
      errorMsg = error.response.data.error
      if (errorMsg.includes('验证码')) {
        codeError.value = errorMsg
      } else if (errorMsg.includes('邮箱')) {
        emailError.value = errorMsg
      } else {
        showErrorMessage(errorMsg)
      }
    } else {
      showErrorMessage(errorMsg)
    }
  } finally {
    isLoading.value = false
  }
}

// 跳转到登录页面
const handleLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 450px;
  animation: fadeInUp 0.6s ease-out;
}

.register-title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  text-align: center;
  margin-bottom: 8px;
}

.register-subtitle {
  font-size: 14px;
  color: #666;
  text-align: center;
  margin-bottom: 32px;
}

.register-form {
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

.code-group {
  position: relative;
}

.code-input-container {
  display: flex;
  gap: 12px;
  align-items: stretch;
}

.code-input {
  flex: 1;
}

.get-code-button {
  padding: 12px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 120px;
}

.get-code-button:hover:not(:disabled) {
  background: #5a6fd8;
  transform: translateY(-1px);
}

.get-code-button:disabled {
  background: #ccc;
  cursor: not-allowed;
  opacity: 0.6;
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

.register-button {
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

.register-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.register-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.register-footer {
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