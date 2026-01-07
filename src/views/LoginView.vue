<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">Offer贝，面试必备</h1>
      <p class="login-subtitle">AI 赋能，让 Offer 更近一步</p>
      
      <div class="login-form">
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
            @keyup.enter="handleLogin"
          />
        </div>
        
        <!-- 密码输入框 -->
        <div class="form-group">
          <div class="password-label-container">
            <label for="password" class="form-label">密码</label>
            <button 
              class="forgot-password-link" 
              @click="handleForgotPassword"
            >
              忘记密码？
            </button>
          </div>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            class="form-input" 
            placeholder="请输入您的密码" 
            required
            @keyup.enter="handleLogin"
          />
        </div>
        
        <!-- 记住我选项 -->
        <div class="remember-me-container">
          <label class="remember-me-label">
            <input 
              type="checkbox" 
              v-model="rememberMe" 
              class="remember-me-checkbox"
            />
            <span class="remember-me-text">记住我</span>
          </label>
        </div>
        
        <!-- 登录按钮 -->
        <button 
          class="login-button" 
          @click="handleLogin"
          :disabled="isLoading || !isFormValid"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
        
        <!-- 注册链接 -->
        <div class="login-footer">
          <p>还没有账号？<button class="register-link" @click="handleRegister">立即注册</button></p>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/utils/api.js'
import ErrorMessage from '@/components/ErrorMessage.vue'

const router = useRouter()
const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const isLoading = ref(false)

// 错误提示相关
const showError = ref(false)
const errorMessage = ref('')
const errorTitle = ref('提示')

// 表单验证
const isFormValid = computed(() => {
  return email.value.trim() && password.value.trim() && isEmailValid(email.value)
})

// 邮箱格式验证
const isEmailValid = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
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

// 处理登录
const handleLogin = async () => {
  if (!isFormValid.value) {
    showErrorMessage('请输入有效的邮箱和密码', '登录失败')
    return
  }
  
  try {
    isLoading.value = true
    // 调用登录API获取令牌
    const response = await apiClient.post('/auth/login', { 
      email: email.value, 
      password: password.value 
    })
    
    // 存储令牌和用户信息
    localStorage.setItem('token', response.data.token)
    localStorage.setItem('userId', response.data.userId || '')
    localStorage.setItem('email', response.data.email)
    
    // 如果选择了记住我，存储到localStorage，否则存储到sessionStorage
    if (rememberMe.value) {
      localStorage.setItem('rememberMe', 'true')
    } else {
      sessionStorage.setItem('token', response.data.token)
      sessionStorage.setItem('userId', response.data.userId || '')
      sessionStorage.setItem('email', response.data.email)
    }

    //打印userId
    // console.log('userId:', response.data.userId)
    // //打印localStorage的userId
    // console.log('localStorage_userID:', localStorage.getItem('userId'))
    //  console.log('sessionStorage_userID:', sessionStorage.getItem('userId'))
    
    // 登录成功后跳转到首页或之前的页面
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
    showErrorMessage(error.response?.data?.error || '登录失败，请重试', '登录失败')
  } finally {
    isLoading.value = false
  }
}

// 处理忘记密码
const handleForgotPassword = () => {
  router.push('/forgot-password')
}

// 处理注册
const handleRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.login-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 40px 30px;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-title {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: #333;
  font-weight: 600;
}

.login-subtitle {
  color: #666;
  margin-bottom: 30px;
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  text-align: left;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.login-button {
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 14px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.login-button:hover:not(:disabled) {
  background-color: #5a6fd8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-footer {
  margin-top: 10px;
  color: #666;
  font-size: 0.9rem;
}

.register-link {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-weight: 600;
  padding: 0;
  margin: 0;
  font-size: 0.9rem;
}

.register-link:hover {
  text-decoration: underline;
}

/* 加载动画 */
.loading-spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
  
  .login-subtitle {
    font-size: 0.9rem;
  }
}
</style>