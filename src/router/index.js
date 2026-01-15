import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: {
        title: 'router.home.title',
        keywords: 'router.home.keywords',
        description: 'router.home.description'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        title: 'router.login.title',
        keywords: 'router.login.keywords',
        description: 'router.login.description'
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: {
        title: 'router.register.title',
        keywords: 'router.register.keywords',
        description: 'router.register.description'
      }
    },
    {
      path: '/forgot-password',
      name: 'forgotPassword',
      component: () => import('../views/ForgotPasswordView.vue'),
      meta: {
        title: 'router.forgotPassword.title',
        keywords: 'router.forgotPassword.keywords',
        description: 'router.forgotPassword.description'
      }
    },
    {
      path: '/reset-password',
      name: 'resetPassword',
      component: () => import('../views/ResetPasswordView.vue'),
      meta: {
        title: 'router.resetPassword.title',
        keywords: 'router.resetPassword.keywords',
        description: 'router.resetPassword.description'
      }
    },
    {
      path: '/resume',
      name: 'resume',
      component: () => import('../views/ResumeView.vue'),
      meta: {
        title: 'router.resume.title',
        keywords: 'router.resume.keywords',
        description: 'router.resume.description'
      }
    },
    {
      path: '/self-intro',
      name: 'selfIntro',
      component: () => import('../views/SelfIntroView.vue'),
      meta: {
        title: 'router.selfIntro.title',
        keywords: 'router.selfIntro.keywords',
        description: 'router.selfIntro.description'
      }
    },
    {
      path: '/question-bank',
      name: 'questionBank',
      component: () => import('../views/QuestionBankView.vue'),
      meta: {
        title: 'router.questionBank.title',
        keywords: 'router.questionBank.keywords',
        description: 'router.questionBank.description'
      }
    },
    {
      path: '/mock-interview',
      name: 'mockInterview',
      component: () => import('../views/MockInterviewView.vue'),
      meta: {
        title: 'router.mockInterview.title',
        keywords: 'router.mockInterview.keywords',
        description: 'router.mockInterview.description'
      }
    },
    {
      path: '/strategy',
      name: 'strategy',
      component: () => import('../views/StrategyView.vue'),
      meta: {
        title: 'router.strategy.title',
        keywords: 'router.strategy.keywords',
        description: 'router.strategy.description'
      }
    },
    {
      path: '/manual',
      name: 'UserManual',
      component: () => import('../views/UserManualView.vue'),
      meta: {
        title: 'router.manual.title',
        keywords: 'router.manual.keywords',
        description: 'router.manual.description'
      }
    },
    {
      path: '/faq',
      name: 'FAQ',
      component: () => import('../views/FAQView.vue'),
      meta: {
        title: 'router.faq.title',
        keywords: 'router.faq.keywords',
        description: 'router.faq.description'
      }
    }
  ]

})

// 路由守卫：公共页面直接放行，保护页面由组件自己处理登录检查
router.beforeEach((to, from, next) => {
  // 动态更新页面标题
  document.title = to.meta.title || 'Offer贝 - 面试必备'

  // 动态更新meta标签
  updateMetaTags(to.meta)

  next()
})

// 更新meta标签的函数
function updateMetaTags(meta) {
  // 更新关键词
  const keywordsMeta = document.querySelector('meta[name="keywords"]')
  if (keywordsMeta && meta.keywords) {
    keywordsMeta.setAttribute('content', meta.keywords)
  }

  // 更新描述
  const descriptionMeta = document.querySelector('meta[name="description"]')
  if (descriptionMeta && meta.description) {
    descriptionMeta.setAttribute('content', meta.description)
  }

  // 更新canonical链接
  let canonicalUrl = window.location.origin
  if (window.location.pathname !== '/') {
    canonicalUrl += window.location.pathname
  }

  let canonicalLink = document.querySelector('link[rel="canonical"]')
  if (canonicalLink) {
    canonicalLink.setAttribute('href', canonicalUrl)
  } else {
    canonicalLink = document.createElement('link')
    canonicalLink.rel = 'canonical'
    canonicalLink.href = canonicalUrl
    document.head.appendChild(canonicalLink)
  }
}

export default router
