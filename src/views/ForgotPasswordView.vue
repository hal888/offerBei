<template>
  <div class="forgot-password-container">
    <div class="forgot-password-card">
      <h1 class="forgot-password-title">Offer贝，面试必备</h1>
      <p class="forgot-password-subtitle">重置您的密码</p>
      <p class="forgot-password-description">请输入您的注册邮箱，我们将向您发送密码重置链接</p>
      
      <div class="forgot-password-form">
        <!-- 邮箱输入框 -->
        <div class="form-group">
          <label for="email" class="form-label">邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            class="form-input" 
            placeholder="请输入您的邮箱" 
            required
            @input="validateEmail"
          />
          <div v-if="emailError" class="error-message">{{ emailError }}</div>
        </div>
        
        <!-- 发送按钮 -->
        <button 
          class="forgot-password-button" 
          @click="handleSendResetLink"
          :disabled="isLoading || emailError || !email.trim()"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? '发送中...' : '发送重置链接' }}
        </button>
        
        <!-- 返回登录链接 -->
        <div class="forgot-password-footer">
          <p>想起密码了？<button class="login-link" @click="handleLogin">返回登录</button></p>
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
import apiClient from '@/utils/api.js'
import ErrorMessage from '@/components/ErrorMessage.vue'

const router = useRouter()
const email = ref('')
const isLoading = ref(false)
const emailError = ref('')

// 错误提示相关
const showError = ref(false)
const errorMessage = ref('')
const errorTitle = ref('提示')
// 错误提示关闭后的回调函数
const errorCloseCallback = ref(null)

// 邮箱验证
const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email.value.trim()) {
    emailError.value = '请输入邮箱'
    return false
  } else if (!emailRegex.test(email.value)) {
    emailError.value = '请输入有效的邮箱格式'
    return false
  } else {
    emailError.value = ''
    return true
  }
}

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

// 发送重置链接
const handleSendResetLink = async () => {
  if (!validateEmail()) return
  
  try {
    isLoading.value = true
    
    // 调用后端API发送重置链接
    await apiClient.post('/auth/request-reset-password', { email: email.value })
    
    // 发送成功，显示提示信息，用户点击确定后跳转到登录页面
    showErrorMessage('密码重置链接已发送，请查收邮件', '发送成功', () => {
      router.push('/login')
    })
  } catch (error) {
    console.error('发送重置链接失败:', error)
    if (error.response?.data?.error) {
      emailError.value = error.response.data.error
    } else {
      showErrorMessage('发送重置链接失败，请重试', '发送失败')
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
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.forgot-password-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 450px;
  animation: fadeInUp 0.6s ease-out;
}

.forgot-password-title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  text-align: center;
  margin-bottom: 8px;
}

.forgot-password-subtitle {
  font-size: 18px;
  color: #333;
  text-align: center;
  margin-bottom: 8px;
}

.forgot-password-description {
  font-size: 14px;
  color: #666;
  text-align: center;
  margin-bottom: 32px;
}

.forgot-password-form {
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

.forgot-password-button {
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

.forgot-password-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.forgot-password-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.forgot-password-footer {
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