<script setup>
// App.vue - Main application component with navigation
import { ref, onMounted, onUnmounted, computed } from 'vue'

// 导航栏显示状态
const navbarVisible = ref(true)
// 导航栏折叠状态
const isNavbarCollapsed = ref(false)
// 上次滚动位置
const lastScrollY = ref(0)
// 滚动阈值，避免微小滚动触发
const scrollThreshold = 10
// 距离顶部阈值
const topThreshold = 50
// 防抖动计时器
let debounceTimer = null
// 滚动动画持续时间
const animationDuration = 200
// 移动设备宽度阈值
const mobileThreshold = 768
// 窗口宽度
const windowWidth = ref(window.innerWidth)

// 计算是否为移动设备视图
const isMobileView = computed(() => {
  return windowWidth.value < mobileThreshold
})

// 滚动事件处理函数
const handleScroll = () => {
  const currentScrollY = window.scrollY
  const scrollDifference = Math.abs(currentScrollY - lastScrollY.value)
  
  // 如果滚动距离小于阈值，不触发状态变化
  if (scrollDifference < scrollThreshold) {
    return
  }
  
  // 清除之前的计时器
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  // 防抖动处理，避免快速连续滚动
  debounceTimer = setTimeout(() => {
    // 页面已处于顶部位置，保持显示
    if (currentScrollY <= topThreshold) {
      navbarVisible.value = true
    } else {
      // 向下滚动时隐藏，向上滚动时显示
      navbarVisible.value = currentScrollY < lastScrollY.value
      // 向下滚动时自动折叠导航栏
      if (currentScrollY > lastScrollY.value && isMobileView.value) {
        isNavbarCollapsed.value = true
      }
    }
    
    // 更新上次滚动位置
    lastScrollY.value = currentScrollY
  }, 50)
}

// 切换导航栏折叠状态
const toggleNavbar = () => {
  if (isMobileView.value) {
    isNavbarCollapsed.value = !isNavbarCollapsed.value
  }
}

// 窗口大小变化事件处理
const handleResize = () => {
  windowWidth.value = window.innerWidth
  // 当窗口从移动视图切换到桌面视图时，自动展开导航栏
  if (!isMobileView.value) {
    isNavbarCollapsed.value = false
  }
}

// 组件挂载时添加事件监听
onMounted(() => {
  // 确保页面加载时导航栏显示
  navbarVisible.value = true
  lastScrollY.value = window.scrollY
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', handleResize)
})

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', handleResize)
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
})
</script>

<template>
  <div class="app-container">
    <!-- Navigation Bar -->
    <nav class="navbar" :class="{ 
      'navbar-hidden': !navbarVisible && window.scrollY > topThreshold,
      'navbar-collapsed': isNavbarCollapsed && isMobileView 
    }">
      <div class="navbar-container">
        <div class="navbar-header">
          <div class="navbar-brand">
            <router-link to="/" class="brand-link">
              <div class="brand-icon">🤖</div>
              <span class="brand-name">AI智能面试宝典</span>
            </router-link>
          </div>
          
          <!-- 移动端折叠按钮 -->
          <button 
            class="navbar-toggle" 
            @click="toggleNavbar"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggle-icon">
              <span v-if="isNavbarCollapsed">☰</span>
              <span v-else>✕</span>
            </span>
          </button>
        </div>
        
        <div class="navbar-menu" :class="{ 'menu-expanded': !isNavbarCollapsed }">
          <router-link to="/" class="nav-link" exact-active-class="active">首页</router-link>
          <router-link to="/resume" class="nav-link" exact-active-class="active">简历优化</router-link>
          <router-link to="/self-intro" class="nav-link" exact-active-class="active">自我介绍</router-link>
          <router-link to="/question-bank" class="nav-link" exact-active-class="active">智能题库</router-link>
          <router-link to="/mock-interview" class="nav-link" exact-active-class="active">模拟面试</router-link>
          <router-link to="/strategy" class="nav-link" exact-active-class="active">面试策略</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-container">
        <p>&copy; 2025 AI智能面试宝典. 保留所有权利.</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  /* 移动端优化字体 */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  /* 响应式字体基础设置 */
  font-size: 16px;
  /* 确保文本对比度符合WCAG AA标准 */
  color: #333333;
  /* 优化行高 */
  line-height: 1.5;
  /* 优化字间距 */
  letter-spacing: 0.01em;
  /* 背景色设置确保对比度 */
  background-color: #ffffff;
}

/* 响应式字体大小 - 基于屏幕宽度 */
@media (max-width: 320px) {
  body {
    font-size: 14px;
  }
}

@media (min-width: 321px) and (max-width: 375px) {
  body {
    font-size: 15px;
  }
}

@media (min-width: 376px) and (max-width: 428px) {
  body {
    font-size: 16px;
  }
}

/* 字体层级结构 */
/* 主标题 */
h1 {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.2;
  color: #2c3e50;
  margin-bottom: 1rem;
}

/* 副标题 */
h2 {
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.3;
  color: #34495e;
  margin-bottom: 0.875rem;
}

/* 三级标题 */
h3 {
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.4;
  color: #34495e;
  margin-bottom: 0.75rem;
}

/* 四级标题 */
h4 {
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1.4;
  color: #34495e;
  margin-bottom: 0.625rem;
}

/* 正文 */
p, span, div {
  font-size: 1rem;
  line-height: 1.5;
  color: #333333;
}

/* 辅助文字 */
.secondary-text {
  font-size: 0.875rem;
  color: #666666;
  line-height: 1.5;
}

/* 小文字 */
.small-text {
  font-size: 0.75rem;
  color: #999999;
  line-height: 1.5;
}

/* 确保正文最小字号 */
*:not(h1):not(h2):not(h3):not(h4):not(h5):not(h6) {
  font-size: clamp(14px, 1rem, 18px);
}

/* 移动端标题响应式调整 */
@media (max-width: 428px) {
  h1 {
    font-size: 1.75rem;
  }
  
  h2 {
    font-size: 1.375rem;
  }
  
  h3 {
    font-size: 1.125rem;
  }
  
  h4 {
    font-size: 1rem;
  }
}

/* App Container */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navigation Bar - 全局一致样式 */
.navbar {
  background-color: #ffffff !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 1000 !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  transition: transform 0.2s ease !important;
  transform: translateY(0);
  /* 确保导航栏层级正确 */
  will-change: transform;
  overflow: hidden;
}

/* 导航栏隐藏状态 */
.navbar.navbar-hidden {
  transform: translateY(-100%);
}

/* 导航栏容器 */
.navbar-container {
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 0 20px !important;
  display: flex !important;
  flex-direction: column !important;
  background-color: transparent !important;
  box-sizing: border-box !important;
  transition: all 0.3s ease !important;
}

/* 导航栏头部 - 包含品牌和切换按钮 */
.navbar-header {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  width: 100% !important;
  padding: 15px 0 !important;
  background-color: transparent !important;
}

/* 移动端折叠按钮 */
.navbar-toggle {
  background: none !important;
  border: none !important;
  cursor: pointer !important;
  padding: 8px !important;
  font-size: 1.5rem !important;
  color: #667eea !important;
  transition: all 0.3s ease !important;
  display: none !important;
}

/* 折叠按钮图标 */
.navbar-toggle-icon {
  display: block !important;
  background-color: transparent !important;
}

/* 导航菜单 */
.navbar-menu {
  display: flex !important;
  gap: 30px !important;
  align-items: center !important;
  background-color: transparent !important;
  transition: all 0.3s ease !important;
  width: 100% !important;
  justify-content: center !important;
  overflow: hidden !important;
  max-height: 500px !important;
}

/* 折叠状态下的菜单 */
.navbar-collapsed .navbar-menu {
  max-height: 0 !important;
  opacity: 0 !important;
  visibility: hidden !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* 展开状态下的菜单 */
.menu-expanded {
  max-height: 500px !important;
  opacity: 1 !important;
  visibility: visible !important;
  padding: 10px 0 !important;
}

/* 确保在桌面端不应用隐藏效果 */
@media (min-width: 769px) {
  .navbar.navbar-hidden {
    transform: translateY(0);
  }
  
  .navbar-container {
    flex-direction: row !important;
    align-items: center !important;
  }
  
  .navbar-menu {
    flex-wrap: wrap !important;
    justify-content: flex-end !important;
  }
  
  .navbar-toggle {
    display: none !important;
  }
}

/* 移动端样式 */
@media (max-width: 768px) {
  .navbar-toggle {
    display: block !important;
  }
  
  .navbar-menu {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 0 !important;
    max-height: 0 !important;
    opacity: 0 !important;
    visibility: hidden !important;
    padding: 0 !important;
  }
  
  .menu-expanded {
    max-height: 500px !important;
    opacity: 1 !important;
    visibility: visible !important;
    padding: 10px 0 !important;
  }
  
  .nav-link {
    display: block !important;
    text-align: center !important;
    padding: 12px 0 !important;
    border-top: 1px solid #f0f0f0 !important;
  }
  
  .nav-link:last-child {
    border-bottom: 1px solid #f0f0f0 !important;
  }
}

.navbar-brand {
  display: flex !important;
  align-items: center !important;
  background-color: transparent !important;
  flex-shrink: 0;
}

.brand-link {
  display: flex !important;
  align-items: center !important;
  gap: 15px !important;
  text-decoration: none !important;
  color: #333 !important;
  font-weight: bold !important;
  background-color: transparent !important;
  flex-shrink: 0;
}

.brand-link:hover {
  color: #333 !important;
  text-decoration: none !important;
  background-color: transparent !important;
}

.brand-icon {
  font-size: 2rem !important;
  background-color: transparent !important;
}

.brand-name {
  font-size: 1.5rem !important;
  color: #667eea !important;
  background-color: transparent !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.navbar-menu {
  display: flex !important;
  gap: 30px !important;
  align-items: center !important;
  background-color: transparent !important;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.nav-link {
  text-decoration: none !important;
  color: #333 !important;
  font-weight: 500 !important;
  font-size: 1rem !important;
  transition: all 0.3s ease !important;
  position: relative !important;
  background-color: transparent !important;
  display: inline-block;
  padding: 8px 0;
  min-width: 80px;
  text-align: center;
}

.nav-link:hover {
  color: #667eea !important;
  text-decoration: none !important;
  background-color: transparent !important;
}

.nav-link.active {
  color: #667eea !important;
  background-color: transparent !important;
}

.nav-link.active::after {
  content: '' !important;
  position: absolute !important;
  bottom: -8px !important;
  left: 0 !important;
  width: 100% !important;
  height: 2px !important;
  background-color: #667eea !important;
  border-radius: 2px !important;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 30px 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

/* Footer */
.footer {
  background-color: #333;
  color: white;
  padding: 20px;
  text-align: center;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Responsive Design */
/* 平板设备优化 */
@media (min-width: 769px) and (max-width: 1024px) {
  .navbar-container {
    padding: 0 15px !important;
  }
  
  .navbar-menu {
    gap: 20px !important;
  }
  
  .main-content {
    padding: 25px 15px;
  }
}

/* 移动设备优化 */
@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    padding: 15px 10px !important;
    gap: 15px;
    align-items: stretch;
  }
  
  .navbar-brand {
    justify-content: center;
  }
  
  .brand-link {
    justify-content: center;
  }
  
  .brand-name {
    font-size: 1.3rem !important;
    max-width: 150px;
  }
  
  .brand-icon {
    font-size: 1.8rem !important;
  }
  
  .navbar-menu {
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px !important;
    padding: 10px 0;
  }
  
  .nav-link {
    font-size: 0.85rem;
    padding: 8px 12px;
    min-width: 70px;
    flex: 1;
    max-width: 120px;
  }
  
  .nav-link.active::after {
    bottom: -6px !important;
    height: 1.5px !important;
  }
  
  .main-content {
    padding: 20px 10px;
  }
}

/* 小屏幕手机优化 */
@media (max-width: 375px) {
  .brand-name {
    font-size: 1.1rem !important;
    max-width: 120px;
  }
  
  .brand-icon {
    font-size: 1.5rem !important;
  }
  
  .navbar-menu {
    gap: 8px !important;
  }
  
  .nav-link {
    font-size: 0.8rem;
    padding: 6px 10px;
    min-width: 65px;
    max-width: 100px;
  }
  
  .brand-link {
    gap: 10px !important;
  }
}
</style>
