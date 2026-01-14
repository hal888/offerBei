<template>
  <div class="faq-container">
    <div class="faq-header">
      <h1>常见问题解答</h1>
      <p class="subtitle">无论是求职疑惑还是产品使用，这里都有您想要的答案</p>
    </div>

    <div class="faq-categories">
      <button 
        v-for="category in categories" 
        :key="category.id"
        :class="['category-btn', { active: activeCategory === category.id }]"
        @click="activeCategory = category.id"
      >
        {{ category.name }}
      </button>
    </div>

    <div class="faq-content">
      <div 
        v-for="(group, index) in filteredGroups" 
        :key="index"
        class="faq-group"
      >
        <h2 class="group-title" v-if="activeCategory === 'all'">{{ group.name }}</h2>
        
        <div class="faq-list">
          <div 
            v-for="(item, qIndex) in group.questions" 
            :key="qIndex"
            class="faq-item"
            :class="{ open: isOpen(group.id, qIndex) }"
            @click="toggle(group.id, qIndex)"
          >
            <div class="faq-question">
              <h3>{{ item.q }}</h3>
              <span class="icon">{{ isOpen(group.id, qIndex) ? '−' : '+' }}</span>
            </div>
            <div class="faq-answer" v-show="isOpen(group.id, qIndex)">
              <div class="answer-content">
                <p v-html="item.a"></p>
                <router-link v-if="item.link" :to="item.link" class="faq-link">立即体验 &rarr;</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="cta-section">
      <h2>准备好开始您的面试之旅了吗？</h2>
      <p>立即注册 Offer贝，解锁您的专属 AI 面试教练</p>
      <router-link to="/register" class="cta-btn">免费注册，开启 Offer 之路</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeCategory = ref('all')
const openItems = ref({}) // key: groupId-questionIndex

const categories = [
  { id: 'all', name: '全部' },
  { id: 'product', name: '关于 Offer贝' },
  { id: 'guide', name: '实操指南' },
  { id: 'scenario', name: '场景化需求' },
  { id: 'comparison', name: '工具对比' }
]

const faqData = [
 
  {
    id: 'product',
    name: '关于 Offer贝',
    questions: [
      {
        q: 'Offer贝 是什么？这个 AI 面试辅助工具怎么用？',
        a: 'Offer贝是一款垂直于求职领域的全流程 AI 面试助手。它不同于通用的聊天机器人，而是专门针对面试场景进行了深度定制。您可以上传简历进行优化，生成个性化自我介绍，刷专项面试题，并进行语音互动的模拟面试。全程由 AI 驱动，随时随地可用。',
        link: '/manual'
      },
      {
        q: 'Offer贝 需要注册吗？有哪些免费功能？',
        a: 'Offer贝提供基础功能的<strong>永久免费</strong>使用权。注册后，您可以免费使用：<br>• 基础简历解析与诊断<br>• 生成标准版自我介绍<br>• 浏览大部分基础面试题<br>• 每日限次体验 AI 模拟面试<br>注册过程仅需手机号，简单快捷。',
        link: '/register'
      },
      {
        q: '我的数据安全吗？AI 会泄露我的简历吗？',
        a: '我们严格遵守隐私保护法规。您的简历仅用于 AI 分析和生成建议，绝不会用于任何商业用途或被公开。'
      }
    ]
  },
  {
    id: 'guide',
    name: '实操指南',
    questions: [
      {
        q: '怎么用 AI 工具模拟技术面试的问答环节？',
        a: '很简单：<br>1. 进入"模拟面试"页面。<br>2. 选择"技术面试"模式和您期望的难度。<br>3. 开启麦克风，AI 会根据您的简历抛出第一个问题。<br>4. 进行语音回答，AI 会实时转录并分析。<br>5. 结束后查看评分报告，查漏补缺。',
        link: '/manual#mock'
      },
      {
        q: '如何利用 AI 优化我的面试作答思路？',
        a: '推荐使用"智能题库"功能。对于每一个问题，Offer贝不仅提供标准答案，还提供<strong>"高分思路"</strong>。您可以先尝试自己回答，然后对比 AI 的解析，学习如何更有逻辑、更由浅入深地组织语言。'
      }
    ]
  },
   {
    id: 'scenario',
    name: '场景化需求',
    questions: [
      {
        q: '应届生/校招新人怎么用 AI 高效准备面试？',
        a: '对于缺乏实战经验的应届生，<strong>Offer贝</strong>建议从两方面入手：<br>1. <strong>高频题库突击</strong>：利用"智能题库"功能，筛选"校招"和"基础"标签，快速掌握八股文。<br>2. <strong>全真模拟</strong>：使用"模拟面试"功能，选择温和风格的 AI 面试官进行多次练习，熟悉面试流程，消除紧张感。',
        link: '/mock-interview'
      },
      {
        q: 'Python/Java/后端开发岗位，如何针对性练习编程题和技术问答？',
        a: 'Offer贝针对技术岗特别优化了题库。您可以上传简历，系统会自动提取您的技术栈（如 Python, Spring Boot, Redis），并生成针对性的技术深挖问题。在模拟面试中，AI 会像真实技术面试官一样，针对您的回答追问底层原理和实现细节。',
        link: '/question-bank'
      },
      {
        q: '面试中常见的行为问题（BQ），AI 工具能指导吗？',
        a: '当然可以。行为面试是 Offer贝的强项之一。系统内置了大量宝洁八大问、STAR 法则相关场景题。AI 会评估您的回答是否逻辑清晰、案例是否具体，并根据 STAR 法则（情境、任务、行动、结果）给出具体的润色建议。'
      }
    ]
  },
  {
    id: 'comparison',
    name: '工具对比与选型',
    questions: [
      {
        q: 'Offer贝 和 ChatGPT、Deepseek、豆包等工具相比，有什么核心优势？',
        a: '通用大模型（如 ChatGPT）虽然全能，但在面试场景下往往缺乏"深度"和"场景感"。<strong>Offer贝的核心优势在于：</strong><br>1. <strong>专业数据微调</strong>：我们使用了海量真实面经对模型进行微调，回答更符合 HR 和技术面试官的口味。<br>2. <strong>结构化流程</strong>：不仅是对话，更是涵盖简历-准备-实战-复盘的全流程闭环。<br>3. <strong>真实交互体验</strong>：提供语音模拟面试和提词器功能，这是纯文本工具无法比拟的。'
      },
      {
        q: '常用的 AI 面试模拟工具对比，Offer贝 适合技术岗吗？',
        a: '非常适合。相比于市面上侧重于销售、客服类岗位的 AI 面试工具，Offer贝特别加强了对<strong>互联网技术岗</strong>（研发、算法、测试、产品）的支持。我们的题库覆盖了主流技术栈，AI 面试官能够理解复杂的代码逻辑和架构设计问题。'
      }
    ]
  }
]

const filteredGroups = computed(() => {
  if (activeCategory.value === 'all') {
    return faqData
  }
  return faqData.filter(group => group.id === activeCategory.value)
})

const toggle = (groupId, index) => {
  const key = `${groupId}-${index}`
  openItems.value[key] = !openItems.value[key]
}

const isOpen = (groupId, index) => {
  return !!openItems.value[`${groupId}-${index}`]
}
</script>

<style scoped>
.faq-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

.faq-header {
  text-align: center;
  margin-bottom: 50px;
}

.faq-header h1 {
  font-size: 2.5rem;
  color: var(--color-text);
  margin-bottom: 15px;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 1.1rem;
  color: var(--color-text-light);
}

.faq-categories {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 50px;
}

.category-btn {
  padding: 10px 24px;
  border-radius: 50px;
  border: 1px solid var(--color-border);
  background: white;
  color: var(--color-text-light);
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.category-btn:hover {
  background: #f8fafc;
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.category-btn.active {
  background: var(--gradient-primary);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.faq-group {
  margin-bottom: 40px;
}

.group-title {
  font-size: 1.5rem;
  color: var(--color-text);
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f1f5f9;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.faq-item {
  background: white;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  overflow: hidden;
  transition: all 0.3s ease;
}

.faq-item:hover {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.faq-item.open {
  border-color: var(--color-primary);
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1);
}

.faq-question {
  padding: 20px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  background: white;
}

.faq-question h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
  line-height: 1.5;
}

.icon {
  font-size: 1.5rem;
  color: var(--color-primary);
  margin-left: 20px;
  font-weight: 300;
  transition: transform 0.3s ease;
}

.faq-item.open .icon {
  transform: rotate(180deg);
}

.faq-answer {
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
}

.answer-content {
  padding: 20px 25px;
  color: var(--color-text-light);
  line-height: 1.7;
  font-size: 1rem;
}

.faq-link {
  display: inline-block;
  margin-top: 15px;
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  font-size: 0.95rem;
  transition: transform 0.2s;
}

.faq-link:hover {
  transform: translateX(4px);
  text-decoration: underline;
}

.cta-section {
  text-align: center;
  margin-top: 80px;
  padding: 60px 40px;
  background: var(--gradient-surface);
  border-radius: 20px;
  border: 1px solid white;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
}

.cta-section h2 {
  font-size: 2rem;
  margin-bottom: 15px;
  color: var(--color-text);
}

.cta-section p {
  color: var(--color-text-light);
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.cta-btn {
  display: inline-block;
  background: var(--gradient-primary);
  color: white;
  padding: 15px 40px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

@media (max-width: 768px) {
  .faq-header h1 {
    font-size: 2rem;
  }
  
  .faq-question {
    padding: 15px 20px;
  }
  
  .faq-question h3 {
    font-size: 1rem;
  }
  
  .cta-section {
    padding: 40px 20px;
  }
  
  .cta-section h2 {
    font-size: 1.5rem;
  }
}
</style>
