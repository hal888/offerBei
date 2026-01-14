<template>
  <div class="manual-container">
    <div class="manual-header">
      <h1>Offer贝 使用手册</h1>
      <p class="subtitle">您的全流程AI面试助手使用指南</p>
    </div>

    <div class="manual-content">
      <nav class="manual-nav">
        <ul>
          <li><a href="#resume" :class="{ active: activeSection === 'resume' }" @click.prevent="scrollTo('resume')">简历优化</a></li>
          <li><a href="#intro" :class="{ active: activeSection === 'intro' }" @click.prevent="scrollTo('intro')">自我介绍</a></li>
          <li><a href="#questions" :class="{ active: activeSection === 'questions' }" @click.prevent="scrollTo('questions')">智能题库</a></li>
          <li><a href="#mock" :class="{ active: activeSection === 'mock' }" @click.prevent="scrollTo('mock')">模拟面试</a></li>
          <li><a href="#strategy" :class="{ active: activeSection === 'strategy' }" @click.prevent="scrollTo('strategy')">面试策略</a></li>
        </ul>
      </nav>

      <div class="manual-sections">
        <section id="resume" class="manual-section">
          <h2>1. 简历解析与智能优化</h2>
          <div class="section-content">
            <p>Offer贝的简历优化功能基于深度学习模型，能够自动识别您的简历结构并提供专业建议。</p>
            <div class="step-list">
              <div class="step-item">
                <span class="step-num">01</span>
                <div class="step-text">
                  <h4>上传简历</h4>
                  <p>点击导航栏的"简历优化"，支持PDF格式的简历文件上传。系统会自动解析您的个人信息、教育背景和工作经历。</p>
                </div>
              </div>
              <div class="step-item">
                <span class="step-num">02</span>
                <div class="step-text">
                  <h4>AI 诊断</h4>
                  <p>系统会从"完整性"、"匹配度"、"竞争力"三个维度对简历进行打分，并指出具体的问题点。</p>
                </div>
              </div>
              <div class="step-item">
                <span class="step-num">03</span>
                <div class="step-text">
                  <h4>一键优化</h4>
                  <p>使用 STAR 法则（情境、任务、行动、结果）重写您的项目经历，自动注入行业高频关键词，显著提升简历含金量。</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="intro" class="manual-section">
          <h2>2. 定制化自我介绍</h2>
          <div class="section-content">
            <p>告别千篇一律的开场白，根据您的简历和目标岗位生成个性化自我介绍。</p>
            <ul class="feature-list">
              <li><strong>多版本生成</strong>：自动生成 30秒（电梯演讲）、3分钟（标准面试）、5分钟（详细介绍）三个版本。</li>
              <li><strong>风格调整</strong>：支持"稳重专业"、"热情活泼"、"创意新颖"等多种风格切换。</li>
              <li><strong>提词器模式</strong>：生成的自我介绍可直接进入提词器模式，支持调节滚动速度和字体大小，方便跟读练习。</li>
            </ul>
          </div>
        </section>

        <section id="questions" class="manual-section">
          <h2>3. 智能题库与定向突击</h2>
          <div class="section-content">
            <p>不再盲目刷题，Offer贝为您提供针对性极强的面试题库。</p>
            <p>进入"智能题库"页面，系统会根据您的简历技能点（如 Java、Python、产品设计等）推荐高频面试题。</p>
            <div class="question-types">
              <div class="type-badge">八股文</div>
              <div class="type-badge">场景题</div>
              <div class="type-badge">算法题</div>
              <div class="type-badge">行为面试(BQ)</div>
            </div>
            <p class="tip">点击题目即可查看参考答案和解析。</p>
          </div>
        </section>

        <section id="mock" class="manual-section">
          <h2>4. 全真模拟真人面试</h2>
          <div class="section-content">
            <p>沉浸式模拟真实面试场景，提升临场应变能力。</p>
            <div class="step-list">
              <div class="step-item">
                <span class="step-num">01</span>
                <div class="step-text">
                  <h4>配置面试官</h4>
                  <p>选择面试官风格（严厉、温和、专业）和面试类型（技术面、HR面、综合面）。</p>
                </div>
              </div>
              <div class="step-item">
                <span class="step-num">02</span>
                <div class="step-text">
                  <h4>实时互动</h4>
                  <p>支持语音实时对话，AI 面试官会根据您的回答进行追问。也支持文字模式输入。</p>
                </div>
              </div>
              <div class="step-item">
                <span class="step-num">03</span>
                <div class="step-text">
                  <h4>复盘报告</h4>
                  <p>面试结束后，生成详细的评估报告，包含维度评分（逻辑性、沟通力、专业度等）和改进建议。</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="strategy" class="manual-section">
          <h2>5. 面试策略锦囊</h2>
          <div class="section-content">
            <p>掌握面试背后的心理博弈，不仅要"答得对"，更要"答得好"。</p>
            <p>在"面试策略"板块，您可以学习：</p>
            <ul>
              <li><strong>谈薪技巧</strong>：如何委婉地争取更高薪资。</li>
              <li><strong>反问环节</strong>：问什么问题能给面试官留下好印象。</li>
              <li><strong>回答陷阱</strong>：如何回答"你的缺点是什么"等送命题。</li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const activeSection = ref('resume')

const scrollTo = (id) => {
  const element = document.getElementById(id)
  if (element) {
    const offset = 80 // Navbar height offset
    const bodyRect = document.body.getBoundingClientRect().top
    const elementRect = element.getBoundingClientRect().top
    const elementPosition = elementRect - bodyRect
    const offsetPosition = elementPosition - offset

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })
    activeSection.value = id
  }
}

const handleScroll = () => {
  const sections = ['resume', 'intro', 'questions', 'mock', 'strategy']
  const scrollPosition = window.scrollY + 100

  for (const section of sections) {
    const element = document.getElementById(section)
    if (element) {
      const top = element.offsetTop
      const height = element.offsetHeight
      
      if (scrollPosition >= top && scrollPosition < top + height) {
        activeSection.value = section
        break
      }
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.manual-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

.manual-header {
  text-align: center;
  margin-bottom: 60px;
}

.manual-header h1 {
  font-size: 2.5rem;
  color: var(--color-text);
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.1rem;
  color: var(--color-text-light);
}

.manual-content {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 40px;
  align-items: start;
}

.manual-nav {
  position: sticky;
  top: 100px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--color-border);
}

.manual-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.manual-nav li {
  margin-bottom: 5px;
}

.manual-nav a {
  display: block;
  padding: 10px 15px;
  color: var(--color-text);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
  font-weight: 500;
}

.manual-nav a:hover,
.manual-nav a.active {
  background-color: #eff6ff;
  color: var(--color-primary);
}

.manual-sections {
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.manual-section {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--color-border);
  scroll-margin-top: 100px;
}

.manual-section h2 {
  font-size: 1.75rem;
  color: var(--color-text);
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f1f5f9;
}

.section-content {
  color: var(--color-text-light);
  line-height: 1.8;
}

.section-content h4 {
  color: var(--color-text);
  margin: 0 0 8px 0;
  font-size: 1.1rem;
}

.step-list {
  display: grid;
  gap: 20px;
  margin-top: 25px;
}

.step-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  align-items: flex-start;
}

.step-num {
  font-size: 1.5rem;
  font-weight: 800;
  color: rgba(102, 126, 234, 0.2);
  line-height: 1;
}

.feature-list {
  margin-top: 20px;
  padding-left: 20px;
}

.feature-list li {
  margin-bottom: 10px;
}

.question-types {
  display: flex;
  gap: 15px;
  margin: 20px 0;
  flex-wrap: wrap;
}

.type-badge {
  padding: 6px 16px;
  background: #eff6ff;
  color: var(--color-primary);
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.tip {
  margin-top: 20px;
  padding: 15px;
  background: #fffbeb;
  border-radius: 8px;
  color: #b45309;
  font-size: 0.95rem;
  border: 1px solid #fcd34d;
}

@media (max-width: 768px) {
  .manual-content {
    grid-template-columns: 1fr;
  }
  
  .manual-nav {
    display: none; /* Hide side nav on mobile */
  }
  
  .manual-section {
    padding: 20px;
  }
  
  .step-item {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
