<script setup>
// App.vue - Main application component with navigation
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Footer from '@/components/Footer.vue'

// 导航栏显示状态
const navbarVisible = ref(true)
// 上次滚动位置
const lastScrollY = ref(0)
// 滚动阈值，避免微小滚动触发
const scrollThreshold = 10
// 距离顶部阈值
const topThreshold = 50
// 防抖动计时器
let debounceTimer = null
// 移动设备宽度阈值
const mobileThreshold = 768
// 窗口宽度
const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)
// 移动端菜单展开状态
const isMenuExpanded = ref(false)
// 获取当前路由
const route = useRoute()
const router = useRouter()
// 用于触发重新计算登录状态的触发器
const loginStatusTrigger = ref(0)

// 计算是否为移动设备视图
const isMobileView = computed(() => {
  return windowWidth.value < mobileThreshold
})

// 切换移动端菜单展开/折叠状态
const toggleMenu = () => {
  isMenuExpanded.value = !isMenuExpanded.value
}

// 关闭移动端菜单
const closeMenu = () => {
  isMenuExpanded.value = false
}

// 滚动事件处理函数
const handleScroll = () => {
  const currentScrollY = typeof window !== 'undefined' ? window.scrollY || 0 : 0
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
    }
    
    // 更新上次滚动位置
    lastScrollY.value = currentScrollY
  }, 50)
}

// 窗口大小变化事件处理
const handleResize = () => {
  windowWidth.value = typeof window !== 'undefined' ? window.innerWidth : windowWidth.value
}

// 计算用户是否已登录
const isUserLoggedIn = computed(() => {
  // 使用loginStatusTrigger作为依赖，强制重新计算
  loginStatusTrigger.value // 触发依赖更新
  return !!localStorage.getItem('token') || !!sessionStorage.getItem('token')
})

// 监听路由变化，当从登录页跳转时，强制刷新登录状态
watch(
  () => route.path,
  (newPath, oldPath) => {
    // 当从登录页或注册页跳转到其他页面时，触发登录状态刷新
    if (oldPath === '/login' || oldPath === '/register') {
      loginStatusTrigger.value++
    }
  }
)

// 监听storage事件，当localStorage或sessionStorage发生变化时，更新登录状态
const handleStorageChange = () => {
  loginStatusTrigger.value++
}

// 组件挂载时添加事件监听
onMounted(() => {
  // 确保页面加载时导航栏显示
  navbarVisible.value = true
  lastScrollY.value = typeof window !== 'undefined' ? window.scrollY || 0 : 0
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', handleResize)
  // 添加storage事件监听
  if (typeof window !== 'undefined') {
    window.addEventListener('storage', handleStorageChange)
  }
})

// 退出登录处理
const handleLogout = () => {
  // 清除本地存储的令牌和用户信息
  localStorage.removeItem('token')
  localStorage.removeItem('userId')
  localStorage.removeItem('email')
  localStorage.removeItem('resumeId')
  
  // 清除会话存储的令牌和用户信息
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('userId')
  sessionStorage.removeItem('email')
  
  // 触发登录状态刷新
  loginStatusTrigger.value++
  
  // 跳转到登录页
  window.location.href = '/login'
}

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', handleResize)
  // 移除storage事件监听
  if (typeof window !== 'undefined') {
    window.removeEventListener('storage', handleStorageChange)
  }
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
})

// i18n
import { useI18n } from 'vue-i18n'
const { t, locale } = useI18n()

const toggleLanguage = () => {
  const newLocale = locale.value === 'zh' ? 'en' : 'zh'
  // 先更新 localStorage，确保 API 拦截器能读取到最新值
  localStorage.setItem('user-locale', newLocale)
  // 再更新 i18n locale
  locale.value = newLocale
  console.log('[Language Toggle] Changed to:', newLocale, '| localStorage:', localStorage.getItem('user-locale'))
}

// 更新页面Meta标签的函数
const updatePageMeta = () => {
  // Update HTML lang attribute
  document.documentElement.lang = locale.value === 'zh' ? 'zh-CN' : 'en-US'

  // Get current route meta
  const meta = route.meta

  // Update Title
  if (meta && meta.title) {
    document.title = t(meta.title)
  } else {
    document.title = t('router.home.title') // Default fallback
  }
  
  // Update Keywords
  const metaKeywords = document.querySelector('meta[name="keywords"]')
  if (metaKeywords) {
    if (meta.keywords) {
      metaKeywords.setAttribute('content', t(meta.keywords))
    } else {
      metaKeywords.setAttribute('content', t('router.home.keywords'))
    }
  }
  
  // Update Description
  const metaDescription = document.querySelector('meta[name="description"]')
  if (metaDescription) {
    if (meta.description) {
      metaDescription.setAttribute('content', t(meta.description))
    } else {
      metaDescription.setAttribute('content', t('router.home.description'))
    }
  }
}

// Watch locale and route to update meta tags
watch([locale, () => route.path], () => {
  updatePageMeta()
})

// 组件挂载后动态插入JSON-LD Schema标记
onMounted(async () => {
  // 同步语言状态：确保 localStorage 和 i18n locale 一致
  // 这对于首次访问的用户非常重要
  const savedLocale = localStorage.getItem('user-locale')
  const currentLocale = locale.value
  
  if (!savedLocale) {
    // 首次访问，localStorage 为空，保存 i18n 检测到的语言
    localStorage.setItem('user-locale', currentLocale)
    console.log('[Language Init] First visit detected. Saved locale to localStorage:', currentLocale)
  } else if (savedLocale !== currentLocale) {
    // localStorage 和 i18n 不一致，以 localStorage 为准（用户上次的选择）
    locale.value = savedLocale
    console.log('[Language Init] Synced locale from localStorage:', savedLocale)
  } else {
    // 已同步，无需操作
    console.log('[Language Init] Locale already synced:', currentLocale)
  }
  
  // 等待router完全准备好后再更新页面Meta
  await router.isReady()
  updatePageMeta()
  
  // 只在浏览器环境中执行
  if (typeof window !== 'undefined') {
    // 创建script标签
    const script = document.createElement('script')
    script.type = 'application/ld+json'
    
    // 设置JSON-LD内容
    const jsonLd = {
      '@context': 'https://schema.org',
      '@type': 'WebApplication',
      'name': 'Offer贝',
      'description': 'AI面试辅助工具，提供简历优化、模拟面试、智能题库等功能，助力求职者拿到心仪Offer',
      'applicationCategory': 'JobSearchingApplication',
      'operatingSystem': 'Web',
      'offers': {
        '@type': 'Offer',
        'price': '0',
        'priceCurrency': 'CNY'
      }
    }
    
    // 将JSON对象转换为字符串
    script.textContent = JSON.stringify(jsonLd)
    
    // 将script标签插入到head标签中
    document.head.appendChild(script)
  }
})
</script>
<!-- 首页添加Schema标记 -->
<template>
  <div class="app-container">
    <!-- Desktop Navigation Bar -->
    <nav class="navbar desktop-navbar" :class="{ 
      'navbar-hidden': !navbarVisible && lastScrollY > topThreshold 
    }">
      <div class="navbar-container">
        <div class="navbar-header">
          <div class="navbar-brand">
            <router-link to="/" class="brand-link" @click="closeMenu">
              <img src="/logo.webp" :alt="t('meta.title')" class="brand-icon" />
              <span class="brand-name">{{ t('nav.brand') }}</span>
            </router-link>
          </div>
          <!-- 移动端折叠按钮 -->
          <button class="navbar-toggle" @click="toggleMenu" aria-label="Toggle navigation">
            <span class="navbar-toggle-icon">{{ isMenuExpanded ? '✕' : '☰' }}</span>
          </button>
        </div>
        
        <div class="navbar-menu" :class="{ 'menu-expanded': isMenuExpanded && isMobileView }">
          <!-- Default Navigation for Visitors -->
          <template v-if="!isUserLoggedIn">
            <router-link to="/" class="nav-link" exact-active-class="active" @click="closeMenu">{{ t('nav.home') }}</router-link>
            
            <!-- Product Features Dropdown -->
            <div class="nav-dropdown">
              <span class="nav-link dropdown-trigger">{{ t('nav.features') }} <i class="icon-down">▾</i></span>
              <div class="dropdown-content">
                <router-link to="/resume" class="dropdown-item" @click="closeMenu">{{ t('nav.resume') }}</router-link>
                <router-link to="/self-intro" class="dropdown-item" @click="closeMenu">{{ t('nav.selfIntro') }}</router-link>
                <router-link to="/question-bank" class="dropdown-item" @click="closeMenu">{{ t('nav.questionBank') }}</router-link>
                <router-link to="/mock-interview" class="dropdown-item" @click="closeMenu">{{ t('nav.mockInterview') }}</router-link>
                <router-link to="/strategy" class="dropdown-item" @click="closeMenu">{{ t('nav.strategy') }}</router-link>
              </div>
            </div>

            <router-link to="/manual" class="nav-link" exact-active-class="active" @click="closeMenu">{{ t('nav.manual') }}</router-link>
          </template>

          <!-- Navigation for Logged-in Users -->
          <template v-else>
            <router-link to="/resume" class="nav-link" exact-active-class="active" @click="closeMenu">{{ t('nav.resume') }}</router-link>
            <router-link to="/self-intro" class="nav-link" exact-active-class="active" @click="closeMenu">{{ t('nav.selfIntro') }}</router-link>
            <router-link to="/question-bank" class="nav-link" exact-active-class="active" @click="closeMenu">{{ t('nav.questionBank') }}</router-link>
            <router-link to="/mock-interview" class="nav-link" exact-active-class="active" @click="closeMenu">{{ t('nav.mockInterview') }}</router-link>
            <router-link to="/strategy" class="nav-link" exact-active-class="active" @click="closeMenu">{{ t('nav.strategy') }}</router-link>
          </template>
          
          <div class="nav-spacer"></div>

          <button class="nav-link lang-btn" @click="toggleLanguage">
            {{ locale === 'zh' ? 'En' : '中' }}
          </button>

          <template v-if="isUserLoggedIn">
            <button class="nav-link logout-btn" @click="handleLogout">{{ t('nav.logout') }}</button>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-link btn-login" @click="closeMenu">{{ t('nav.loginRegister') }}</router-link>
          </template>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" v-if="Component" :key="route.path" />
        </keep-alive>
      </router-view>
    </main>



    <Footer />
  </div>
</template>

<style scoped>
/* App Container */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navigation Bar - 全局一致样式 */
.navbar {
  background-color: var(--color-bg) !important;
  box-shadow: 0 2px 20px rgba(102, 126, 234, 0.15) !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 1000 !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  transition: all 0.3s ease !important;
  transform: translateY(0);
  backdrop-filter: blur(15px) saturate(110%);
  background-color: rgba(255, 255, 255, 0.98) !important;
  /* 确保导航栏层级正确 */
  will-change: transform;
  overflow: visible !important;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

/* 导航栏隐藏状态 */
.navbar.navbar-hidden {
  transform: translateY(-100%);
}

/* 导航栏容器 */
.navbar-container {
  max-width: var(--content-max) !important;
  margin: 0 auto !important;
  padding: 0 20px !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: space-between !important;
  background-color: transparent !important;
  box-sizing: border-box !important;
  transition: all 0.3s ease !important;
  width: 100% !important;
  gap: 20px !important;
}

/* 导航栏头部 - 包含品牌和切换按钮 */
.navbar-header {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 15px 0 !important;
  background-color: transparent !important;
  flex-shrink: 0 !important;
}

/* 移动端折叠按钮 */
.navbar-toggle {
  background: none !important;
  border: none !important;
  cursor: pointer !important;
  padding: 8px !important;
  font-size: 1.5rem !important;
  color: var(--color-primary) !important;
  transition: all 0.3s ease !important;
  display: none !important;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  margin-left: auto !important;
}

/* 折叠按钮图标 */
.navbar-toggle-icon {
  display: block !important;
  background-color: transparent !important;
}

/* 折叠按钮悬停效果 */
.navbar-toggle:hover {
  background-color: rgba(102, 126, 234, 0.1);
  transform: rotate(90deg);
}

/* 导航菜单 */
.navbar-menu {
  display: flex !important;
  gap: 25px !important;
  align-items: center !important;
  background-color: transparent !important;
  transition: all 0.3s ease !important;
  flex: 1 !important;
  justify-content: flex-end !important;
  max-height: 500px !important;
  flex-wrap: nowrap !important;
  overflow: visible !important;
}

/* 折叠状态下的菜单 */
.navbar-menu {
  max-height: 500px !important;
  opacity: 1 !important;
  visibility: visible !important;
  padding: 0 !important;
  margin: 0 !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 移动端菜单默认状态 */
@media (max-width: 1024px) {
  .navbar-menu {
    flex-wrap: wrap !important;
    gap: 15px !important;
  }
}

/* 移动端菜单折叠状态 */
@media (max-width: 768px) {
  .navbar-menu {
    max-height: 0 !important;
    opacity: 0 !important;
    visibility: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 10px !important;
  }
}

/* 展开状态下的菜单 */
.menu-expanded {
  max-height: 800px !important;
  opacity: 1 !important;
  visibility: visible !important;
  padding: 25px 0 !important;
  margin: 0 !important;
  flex-direction: column !important;
  align-items: stretch !important;
  gap: 15px !important;
  background-color: rgba(255, 255, 255, 0.98) !important;
  border-radius: 0 0 16px 16px !important;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15) !important;
  backdrop-filter: blur(15px) saturate(110%) !important;
  overflow: visible !important;
}

/* 确保菜单展开状态在移动端正确应用 */
@media (max-width: 768px) {
  .menu-expanded {
    max-height: 800px !important;
    opacity: 1 !important;
    visibility: visible !important;
    padding: 25px 0 !important;
    margin: 0 !important;
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 15px !important;
  }
}

/* 桌面端导航样式 */
.desktop-navbar {
  display: block;
}

/* 移动端顶部品牌 */
.mobile-top-brand {
  display: none;
  background-color: rgba(255, 255, 255, 0.98);
  box-shadow: 0 2px 20px rgba(102, 126, 234, 0.15);
  padding: 15px 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
  padding-top: env(safe-area-inset-top);
  backdrop-filter: blur(15px) saturate(110%);
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

/* 品牌内容容器 */
.brand-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

/* 移动端底部导航在桌面端默认隐藏 */
.mobile-navbar {
  display: none;
}

/* 超宽屏幕样式 */
@media (min-width: 1440px) {
  .navbar-container {
    max-width: 1350px !important;
    padding: 0 30px !important;
  }
  
  .navbar-menu {
    gap: 30px !important;
  }
  
  .nav-link {
    font-size: 1.05rem !important;
    padding: 12px 20px !important;
  }
}

/* 桌面端样式 */
@media (min-width: 1025px) {
  .navbar.navbar-hidden {
    transform: translateY(0);
  }
  
  .navbar-container {
    flex-direction: row !important;
    align-items: center !important;
    flex-wrap: nowrap !important;
    justify-content: space-between !important;
  }
  
  .navbar-header {
    flex: 0 0 auto !important;
  }
  
  .navbar-menu {
    flex: 1 !important;
    flex-wrap: nowrap !important;
    justify-content: flex-end !important;
    gap: 25px !important;
    overflow: visible !important;
  }
  
  .navbar-toggle {
    display: none !important;
  }
  /* 桌面端隐藏底部导航栏 */
  .mobile-navbar {
    display: none !important;
  }
}

/* 平板设备样式 */
@media (min-width: 769px) and (max-width: 1024px) {
  .navbar-container {
    padding: 0 15px !important;
    flex-wrap: nowrap !important;
  }
  
  .navbar-menu {
    gap: 18px !important;
    flex-wrap: nowrap !important;
    overflow: visible !important;
  }
  
  .nav-link {
    padding: 10px 15px !important;
    font-size: 0.95rem !important;
    min-width: 80px !important;
  }
  
  .navbar-toggle {
    display: none !important;
  }
  
  .mobile-navbar {
    display: none !important;
  }
}

/* 移动端样式 */
@media (max-width: 768px) {
  /* 调整桌面端导航显示方式 */
  .desktop-navbar {
    display: block !important;
  }
  
  /* 显示移动端折叠按钮 */
  .navbar-toggle {
    display: flex !important;
    font-size: 2rem !important;
    width: 50px !important;
    height: 50px !important;
  }
  
  /* 调整导航栏容器 */
  .navbar-container {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 15px !important;
    padding: 15px 20px !important;
  }
  
  /* 调整导航菜单 */
  .navbar-menu {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 15px !important;
    padding: 0 !important;
  }
  
  /* 调整导航链接 */
  /* 调整导航链接 */
  /* 调整导航链接 */
  .nav-link {
    font-size: 1rem !important; /* Unified font size */
    padding: 16px 20px !important;
    text-align: center !important;
    width: 100% !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    color: var(--color-text) !important;
    font-family: var(--font-sans) !important;
    border-bottom: 1px solid rgba(0,0,0,0.03) !important;
    margin-bottom: 4px !important;
  }

  /* 移除最后一个链接的边框 */
  .nav-link:last-child {
    border-bottom: none !important;
  }
  
  /* 优化退出登录按钮样式 */
  .nav-link.logout-btn {
    font-size: 1rem !important; /* Unified font size */
    padding: 16px 20px !important;
    font-weight: 600 !important;
    background-color: rgba(102, 126, 234, 0.05) !important;
    border-color: var(--color-primary) !important;
    color: var(--color-primary) !important;
    border-radius: 12px !important;
    margin-top: 10px !important;
  }
  
  /* 显示移动端顶部品牌 */
  .mobile-top-brand {
    display: none !important;
  }
  
  /* 移除移动端底部导航样式 */
  .mobile-navbar {
    display: none !important;
  }
  
  /* 调整主内容区 */
  .main-content {
    padding-bottom: 0 !important;
  }
  
  /* 调整移动端footer */
  .footer {
    margin-bottom: 0 !important;
  }

  /* 小屏幕手机优化 */
  @media (max-width: 375px) {
    .navbar-toggle {
      font-size: 1.8rem !important;
      width: 45px !important;
      height: 45px !important;
    }
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
  color: var(--color-text) !important;
  font-weight: bold !important;
  background-color: transparent !important;
  flex-shrink: 0;
  transition: all 0.3s ease !important;
  padding: 8px 12px !important;
  border-radius: 12px !important;
  position: relative;
  overflow: hidden;
}

.brand-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.brand-link:hover {
  color: var(--color-primary) !important;
  text-decoration: none !important;
  background-color: transparent !important;
  transform: translateY(-2px) scale(1.02) !important;
}

.brand-link:hover::before {
  opacity: 1;
}

.brand-link:hover .brand-name {
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-link:hover .brand-icon {
  transform: scale(1.1) rotate(5deg);
}

.brand-icon {
  width: 40px !important;
  height: 40px !important;
  background-color: transparent !important;
  object-fit: contain;
  transition: all 0.3s ease !important;
  position: relative;
  z-index: 1;
}

.brand-name {
  font-size: 1.5rem !important;
  color: var(--color-primary) !important;
  background-color: transparent !important;
  white-space: nowrap;
  overflow: visible;
  text-overflow: clip;
  max-width: none;
  flex-shrink: 0;
  font-weight: 700 !important;
  transition: all 0.3s ease !important;
  position: relative;
  z-index: 1;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 4px rgba(102, 126, 234, 0.1);
}

.navbar-menu {
  display: flex !important;
  gap: 30px !important;
  align-items: center !important;
  background-color: transparent !important;
  flex-wrap: nowrap;
  justify-content: flex-end;
}


.nav-link {
  text-decoration: none !important;
  color: var(--color-text-secondary) !important;
  font-weight: 500 !important;
  font-size: 1rem !important;
  transition: all 0.3s ease !important;
  position: relative !important;
  background-color: transparent !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 12px 16px !important;
  min-width: unset !important; /* Allow variable width */
  text-align: center !important;
  border-radius: 8px !important;
  border: 2px solid transparent !important;
  box-sizing: border-box !important;
  overflow: visible !important; /* Allow dropdown to show */
  cursor: pointer !important;
}

.nav-link:not(.btn-login):not(.btn-register):not(.dropdown-trigger):hover {
  color: var(--color-primary) !important;
  background-color: rgba(102, 126, 234, 0.08) !important;
}

.nav-link.active {
  color: var(--color-primary) !important;
  font-weight: 600 !important;
}

/* Spacer to push login/register to right */
.nav-spacer {
  flex-grow: 1;
}

/* Dropdown Styles */
.nav-dropdown {
  position: relative;
  display: inline-flex;
  align-items: center;
  height: 100%;
}

.dropdown-trigger {
  cursor: pointer;
  gap: 4px;
}

.icon-down {
  font-size: 0.8em;
  transition: transform 0.3s ease;
  display: inline-block;
}

.nav-dropdown:hover .icon-down {
  transform: rotate(180deg);
}

.dropdown-content {
  display: none;
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: white;
  min-width: 160px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  border-radius: 12px;
  padding: 8px 0;
  z-index: 1001;
  border: 1px solid rgba(0,0,0,0.05);
  margin-top: 5px;
}

.nav-dropdown::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  height: 15px;
  background: transparent;
}

.nav-dropdown:hover .dropdown-content {
  display: block;
  animation: fadeIn 0.2s ease;
}

.dropdown-item {
  display: block;
  padding: 10px 20px;
  text-decoration: none;
  color: var(--color-text);
  transition: all 0.2s;
  font-size: 0.95rem;
  text-align: left;
  white-space: nowrap;
}

.dropdown-item:hover {
  background-color: #f8fafc;
  color: var(--color-primary);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translate(-50%, 10px); }
  to { opacity: 1; transform: translate(-50%, 0); }
}

/* Auth Buttons */
.btn-login, .btn-register {
  padding: 10px 24px !important;
  border-radius: 50px !important;
  font-weight: 600 !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  min-width: 80px !important;
}

.btn-login {
  color: var(--color-primary) !important;
  border: 1px solid var(--color-primary) !important;
  background-color: transparent !important;
  margin-left: 20px;
}

.btn-login:hover {
  background-color: rgba(102, 126, 234, 0.1) !important;
  transform: translateY(-2px) !important;
}

.btn-register {
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary)) !important;
  color: white !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
}

.btn-register:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4) !important;
  color: white !important;
}



/* 移除旧的下划线样式，使用边框和背景色替代 */
.nav-link.active::after {
  content: '' !important;
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  height: 2px !important;
  background-color: var(--color-primary) !important;
  border-radius: 0 0 4px 4px !important;
  z-index: 2 !important;
}

/* 为导航链接添加顶部装饰条作为视觉指示器 */
.nav-link::before {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  width: 0 !important;
  height: 3px !important;
  background-color: var(--color-primary) !important;
  border-radius: 3px 3px 0 0 !important;
  transition: all 0.3s ease !important;
  z-index: 1 !important;
}

.nav-link:hover::before,
.nav-link.active::before {
  width: 100% !important;
  left: 0 !important;
  transform: translateX(0) !important;
  border-radius: 0 !important;
}

/* 确保底部边框完全覆盖 */
.nav-link.active {
  position: relative !important;
  z-index: 1 !important;
  /* 移除重复的border-bottom，只使用::after伪元素 */
  border-bottom: none !important;
}

/* 登录、注册、退出按钮样式 */
.nav-link.login-btn {
  background-color: rgba(102, 126, 234, 0.1) !important;
  border-color: var(--color-primary) !important;
  color: var(--color-primary) !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
  white-space: nowrap !important;
  min-width: 80px !important;
}

.nav-link.login-btn:hover {
  background-color: rgba(102, 126, 234, 0.2) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
}

.nav-link.register-btn {
  background-color: var(--color-primary) !important;
  border-color: var(--color-primary) !important;
  color: white !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
  white-space: nowrap !important;
  min-width: 80px !important;
}

.nav-link.register-btn:hover {
  background-color: var(--color-secondary) !important;
  border-color: var(--color-secondary) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
}

.nav-link.logout-btn {
  background-color: rgba(102, 126, 234, 0.1) !important;
  border-color: var(--color-primary) !important;
  color: var(--color-primary) !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: all 0.3s ease !important;
  white-space: nowrap !important;
  min-width: 100px !important;
  position: relative !important;
}

.nav-link.logout-btn:hover {
  background-color: rgba(102, 126, 234, 0.2) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
}

/* 登录、注册、退出按钮激活状态样式 */
.nav-link.login-btn.active,
.nav-link.register-btn.active,
.nav-link.logout-btn.active {
  /* 移除重复的border-bottom，只使用::after伪元素 */
  border-bottom: none !important;
  background-color: rgba(102, 126, 234, 0.1) !important;
  border-color: var(--color-primary) !important;
  font-weight: 600 !important;
  box-shadow: 0 2px 12px rgba(102, 126, 234, 0.25) !important;
  transform: translateY(-2px) !important;
  padding-bottom: 12px !important;
}

/* 登录、注册、退出按钮的底部遮盖层 - 确保完全覆盖 */
.nav-link.login-btn.active::after,
.nav-link.register-btn.active::after,
.nav-link.logout-btn.active::after {
  content: '' !important;
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  height: 2px !important;
  background-color: var(--color-primary) !important;
  border-radius: 0 0 4px 4px !important;
  z-index: 2 !important;
  /* 确保完全覆盖整个按钮宽度 */
  width: 100% !important;
}

/* 移除登录、注册、退出按钮的顶部装饰条 */
.nav-link.login-btn::before,
.nav-link.register-btn::before,
.nav-link.logout-btn::before,
.nav-link.lang-btn::before {
  content: none !important;
}

.nav-link.lang-btn {
  font-family: inherit;
  font-size: 0.95rem;
  padding: 8px 16px;
  cursor: pointer;
}

/* 确保所有导航链接文字不换行 */
.nav-link {
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  min-width: 85px !important;
  /* 确保文字始终在一行显示 */
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}

/* 屏幕较小时优化字体大小和间距 */
@media (max-width: 1200px) {
  .navbar-menu {
    gap: 20px !important;
  }
  
  .nav-link {
    font-size: 0.95rem !important;
    padding: 10px 14px !important;
  }
}

@media (max-width: 1024px) {
  .navbar-menu {
    gap: 15px !important;
  }
  
  .nav-link {
    font-size: 0.9rem !important;
    padding: 10px 12px !important;
    min-width: 80px !important;
  }
  
  .nav-link.logout-btn {
    min-width: 90px !important;
  }
}

@media (max-width: 900px) {
  .navbar-menu {
    gap: 12px !important;
  }
  
  .nav-link {
    font-size: 0.85rem !important;
    padding: 8px 10px !important;
    min-width: 75px !important;
  }
  
  .nav-link.logout-btn {
    min-width: 85px !important;
  }
}

@media (max-width: 800px) {
  .navbar-menu {
    gap: 10px !important;
  }
  
  .nav-link {
    font-size: 0.8rem !important;
    padding: 8px 8px !important;
    min-width: 70px !important;
  }
  
  .nav-link.logout-btn {
    min-width: 80px !important;
  }
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 30px 20px;
  max-width: var(--content-max);
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}


/* Responsive Design */
/* 平板设备优化 */
@media (min-width: 769px) and (max-width: 1024px) {
  .navbar-container {
    padding: 0 15px !important;
    flex-wrap: nowrap !important;
  }
  
  .navbar-menu {
    gap: 15px !important;
    flex-wrap: nowrap !important;
    overflow: visible !important;
  }
  
  .nav-link {
    padding: 10px 12px !important;
    font-size: 0.9rem !important;
  }
  
  .main-content {
    padding: 25px 15px;
  }
}



/* 小屏幕手机优化 */
  @media (max-width: 375px) {
    .brand-name {
      font-size: 1.1rem !important;
      max-width: none;
      overflow: visible;
      text-overflow: clip;
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

/* Mobile Optimizations for Dropdown and Auth */
@media (max-width: 768px) {
  /* Flatten dropdown in mobile menu */
  .nav-dropdown {
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    height: auto !important;
  }

  /* Hide trigger text on mobile, just show items */
  .dropdown-trigger {
    display: none !important;
  }

  .dropdown-content {
    display: flex !important;
    position: static !important;
    flex-direction: column !important;
    width: 100% !important;
    box-shadow: none !important;
    border: none !important;
    background: transparent !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
    min-width: unset !important;
    opacity: 1 !important;
  }

  .dropdown-item {
    font-size: 1.1rem !important;
    padding: 16px 20px !important;
    text-align: center !important;
    width: 100% !important;
    box-sizing: border-box !important;
    border-radius: 12px !important;
    color: var(--color-text-secondary) !important; /* Slightly lighter for sub-items */
    font-weight: 500 !important;
    border-bottom: 1px solid rgba(0,0,0,0.03) !important;
    margin-bottom: 4px !important;
  }
  
  .dropdown-item:hover {
    background-color: rgba(102, 126, 234, 0.08) !important;
    color: var(--color-primary) !important;
    padding-left: 20px !important; /* Prevent shift on mobile */
  }

  /* Adjust Auth Buttons for Mobile */
  .btn-login, .btn-register {
    width: 90% !important;
    margin: 8px auto !important;
    padding: 14px 0 !important;
    font-size: 1.1rem !important;
    border-radius: 50px !important;
  }
  
  .btn-login {
    margin-left: 0 !important;
    margin-top: 20px !important; /* Separate from menu */
  }
}
