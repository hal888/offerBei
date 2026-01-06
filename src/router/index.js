import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: {
        title: 'Offer贝，面试必备',
        keywords: 'Offer贝,面试必备,简历优化,模拟面试,智能题库,自我介绍,面试策略,AI面试',
        description: 'Offer贝，面试必备，一站式解决求职者"简历差、不会说、没题练、怕面试"的四大痛点，提供简历优化、模拟面试、智能题库等功能'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        title: '登录 - Offer贝',
        keywords: 'Offer贝登录,面试工具登录,简历优化登录,模拟面试登录',
        description: '登录Offer贝，使用简历优化、模拟面试、智能题库等功能'
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: {
        title: '注册 - Offer贝',
        keywords: 'Offer贝注册,面试工具注册,简历优化注册,模拟面试注册',
        description: '注册Offer贝账号，免费使用简历优化、模拟面试、智能题库等功能'
      }
    },
    {
      path: '/forgot-password',
      name: 'forgotPassword',
      component: () => import('../views/ForgotPasswordView.vue'),
      meta: {
        title: '忘记密码 - Offer贝',
        keywords: 'Offer贝忘记密码,面试工具找回密码,简历优化重置密码',
        description: 'Offer贝密码找回，重置您的账号密码'
      }
    },
    {
      path: '/reset-password',
      name: 'resetPassword',
      component: () => import('../views/ResetPasswordView.vue'),
      meta: {
        title: '重置密码 - Offer贝',
        keywords: 'Offer贝重置密码,面试工具修改密码,简历优化密码设置',
        description: 'Offer贝密码重置，设置新的账号密码'
      }
    },
    {
      path: '/resume',
      name: 'resume',
      component: () => import('../views/ResumeView.vue'),
      meta: {
        title: '简历解析与智能优化 - Offer贝',
        keywords: '简历优化,简历解析,智能简历,STAR法则,简历评分,简历关键词,ATS优化,简历下载',
        description: 'Offer贝简历优化，自动识别简历结构，智能诊断问题，提供STAR法则重写和关键词注入，提升简历竞争力'
      }
    },
    {
      path: '/self-intro',
      name: 'selfIntro',
      component: () => import('../views/SelfIntroView.vue'),
      meta: {
        title: '定制化自我介绍生成 - Offer贝',
        keywords: '自我介绍,自我介绍生成,定制化自我介绍,面试自我介绍,30秒自我介绍,3分钟自我介绍,提词器',
        description: 'Offer贝自我介绍生成，根据简历自动生成30秒、3分钟、5分钟多版本自我介绍，支持口语化处理和提词器模式'
      }
    },
    {
      path: '/question-bank',
      name: 'questionBank',
      component: () => import('../views/QuestionBankView.vue'),
      meta: {
        title: '智能题库与定向突击 - Offer贝',
        keywords: '智能题库,面试题库,定向突击,高频必问题,简历深挖题,专业技能题,行为情景题,模拟题库',
        description: 'Offer贝智能题库，提供30题、50题、100题三种模式，涵盖高频必问题、简历深挖题、专业技能题和行为情景题'
      }
    },
    {
      path: '/mock-interview',
      name: 'mockInterview',
      component: () => import('../views/MockInterviewView.vue'),
      meta: {
        title: '全真模拟真人面试 - Offer贝',
        keywords: '模拟面试,AI面试,全真面试,面试官风格,语音交互,文字交互,多轮追问,面试复盘,面试报告',
        description: 'Offer贝模拟面试，支持多种面试官风格选择，语音/文字交互模式，智能多轮追问和复盘报告，提升面试能力'
      }
    },
    {
      path: '/strategy',
      name: 'strategy',
      component: () => import('../views/StrategyView.vue'),
      meta: {
        title: '面试策略锦囊 - Offer贝',
        keywords: '面试策略,面试技巧,劣势防御,防御性话术,高质量反问,面试准备,面试成功,面试经验',
        description: 'Offer贝面试策略，提供劣势识别和防御性话术，生成高质量反问问题，助力面试成功'
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
