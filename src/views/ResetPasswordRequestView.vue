<template>
  <div class="reset-container">
    <div class="reset-card">
      <h1 class="reset-title">{{ t('auth.forgot.title') }}</h1>
      <p class="reset-subtitle">{{ t('auth.forgot.subtitle') }}</p>
      <p class="reset-description">{{ t('auth.forgot.desc') }}</p>
      
      <div class="reset-form">
        <!-- 邮箱输入框 -->
        <div class="form-group">
          <label for="email" class="form-label">{{ t('auth.login.emailLabel') }}</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            class="form-input" 
            :placeholder="t('auth.login.emailPlaceholder')" 
            required
            @input="validateEmail"
          />
          <div v-if="emailError" class="error-message">{{ emailError }}</div>
        </div>
        
        <!-- 发送按钮 -->
        <button 
          class="reset-button" 
          @click="handleSendResetLink"
          :disabled="isLoading || emailError || !email.trim()"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? t('auth.forgot.sending') : t('auth.forgot.sendBtn') }}
        </button>
        
        <!-- 返回登录链接 -->
        <div class="reset-footer">
          <p>{{ t('auth.forgot.remembered') }}<button class="login-link" @click="handleLogin">{{ t('auth.forgot.loginLink') }}</button></p>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import apiClient from '@/utils/api.js'
import ErrorMessage from '@/components/ErrorMessage.vue'

const router = useRouter()
const { t, locale } = useI18n()
const email = ref('')
const isLoading = ref(false)
const emailError = ref('')

// 错误提示相关
const showError = ref(false)
const errorMessage = ref('')
const errorTitle = ref('提示')

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

// 显示错误信息
const showErrorMessage = (message, title = '提示') => {
  errorMessage.value = message
  errorTitle.value = title
  showError.value = true
}

// 关闭错误信息
const closeError = () => {
  showError.value = false
  errorMessage.value = ''
  errorTitle.value = '提示'
}

// 发送重置链接
const handleSendResetLink = async () => {
  if (!validateEmail()) return
  
  try {
    isLoading.value = true
    
    // 调用后端API发送重置链接
    await apiClient.post('/auth/request-reset-password', { 
      email: email.value,
      locale: locale.value
    })
    
    // 发送成功，跳转到登录页面并提示
    showErrorMessage(t('auth.forgot.success'), t('auth.forgot.success'))
    // 1秒后跳转到登录页面
    setTimeout(() => {
      router.push('/login')
    }, 1000)
  } catch (error) {
    console.error('发送重置链接失败:', error)
    if (error.response?.data?.error) {
      emailError.value = error.response.data.error
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
