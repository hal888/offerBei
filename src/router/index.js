import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: {
        title: 'Offer贝 - AI智能模拟面试 | 免费简历优化与自我介绍生成器',
        keywords: 'Offer贝,AI面试,模拟面试,简历优化,自我介绍生成,面试题库,求职辅助',
        description: 'Offer贝利用先进AI技术，为您提供专业的简历优化建议、个性化模拟面试、海量智能题库及面试策略分析，助您轻松拿到心仪Offer。'
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
        title: '简历优化 - AI智能诊断与润色 | Offer贝',
        keywords: '简历优化,简历修改,AI改简历,STAR法则,简历诊断,简历润色',
        description: '上传简历，AI自动分析亮点与不足，提供STAR法则重写建议，一键生成专业简历，提升简历通过率。'
      }
    },
    {
      path: '/self-intro',
      name: 'selfIntro',
      component: () => import('../views/SelfIntroView.vue'),
      meta: {
        title: '自我介绍生成器 - 30秒/3分钟多版本 | Offer贝',
        keywords: '自我介绍生成,面试自我介绍,3分钟自我介绍,AI写自我介绍,面试提词器',
        description: '输入简历，AI自动生成不同时长的面试自我介绍，支持口语化处理和提词器模式，助您克服面试紧张。'
      }
    },
    {
      path: '/question-bank',
      name: 'questionBank',
      component: () => import('../views/QuestionBankView.vue'),
      meta: {
        title: 'AI智能面试题库 - 高频真题与解析 | Offer贝',
        keywords: '面试题库,Java面试题,前端面试题,AI出题,个性化面试题,高频面试题',
        description: '海量互联网面试真题，涵盖Java, Python, 前端等技术栈，基于简历生成个性化面试题，提供深度解析与参考答案。'
      }
    },
    {
      path: '/mock-interview',
      name: 'mockInterview',
      component: () => import('../views/MockInterviewView.vue'),
      meta: {
        title: 'AI模拟面试 - 真实场景演练 | Offer贝',
        keywords: '模拟面试,AI面试官,语音面试,面试练手,面试复盘,真实面试体验',
        description: '全真模拟面试环境，支持语音交互，AI面试官实时反馈，提供多维度面试报告，助您提升面试实战能力。'
      }
    },
    {
      path: '/strategy',
      name: 'strategy',
      component: () => import('../views/StrategyView.vue'),
      meta: {
        title: '面试攻略与技巧 - 薪资谈判与避坑指南 | Offer贝',
        keywords: '面试攻略,面试技巧,薪资谈判,面试避坑,面试反问,求职指导',
        description: '提供全面的面试攻略，包括薪资谈判技巧、常见陷阱规避、反问环节指导等，助您掌握面试主动权。'
      }
    },
    {
      path: '/manual',
      name: 'UserManual',
      component: () => import('../views/UserManualView.vue'),
      meta: {
        title: '使用手册 - Offer贝',
        keywords: 'Offer贝使用手册,面试工具指南,简历优化教程,模拟面试教程',
        description: 'Offer贝全流程AI面试助手使用指南，教您如何高效使用简历优化、模拟面试、智能题库等功能。'
      }
    },
    {
      path: '/faq',
      name: 'FAQ',
      component: () => import('../views/FAQView.vue'),
      meta: {
        title: '常见问题解答 - Offer贝',
        keywords: 'Offer贝常见问题,AI面试疑问,求职辅助工具,面试模拟QA',
        description: '解答关于Offer贝的常见问题，包括产品功能、使用方法、隐私安全及面试技巧指导，助您更好地使用AI面试助手。'
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
