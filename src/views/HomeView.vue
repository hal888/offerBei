<template>
  <div class="home-container">
    <header class="hero-section">
      <div class="hero-content">
        <h1>Offer贝，面试必备</h1>
        <p>一站式解决求职者"简历差、不会说、没题练、怕面试"的四大痛点</p>
        <div class="cta-buttons">
          <router-link to="/resume" class="btn primary-btn">开始使用</router-link>
          <router-link to="/mock-interview" class="btn secondary-btn">模拟面试</router-link>
        </div>
      </div>
    </header>

    <section class="features-section">
      <h2>核心功能</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon resume-icon"></div>
          <h3>简历解析与智能优化</h3>
          <p>自动识别简历结构，智能诊断问题，提供STAR法则重写和关键词注入</p>
          <router-link to="/resume" class="learn-more">了解更多</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon intro-icon"></div>
          <h3>定制化自我介绍生成</h3>
          <p>生成30秒、3分钟、5分钟多版本自我介绍，支持口语化处理和提词器模式</p>
          <router-link to="/self-intro" class="learn-more">了解更多</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon bank-icon"></div>
          <h3>智能题库与定向突击</h3>
          <p>提供30题、50题、100题三种模式，涵盖高频必问题、简历深挖题、专业技能题和行为情景题</p>
          <router-link to="/question-bank" class="learn-more">了解更多</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon mock-icon"></div>
          <h3>全真模拟真人面试</h3>
          <p>支持多种面试官风格选择，语音/文字交互模式，智能多轮追问和复盘报告</p>
          <router-link to="/mock-interview" class="learn-more">了解更多</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon strategy-icon"></div>
          <h3>面试策略锦囊</h3>
          <p>提供劣势识别和防御性话术，生成高质量反问问题，助力面试成功</p>
          <router-link to="/strategy" class="learn-more">了解更多</router-link>
        </div>
      </div>
    </section>

    <section class="process-section">
      <h2>使用流程</h2>
      <div class="process-steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3>上传简历</h3>
          <p>支持PDF格式</p>
        </div>
        <div class="step-arrow">→</div>
        <div class="step">
          <div class="step-number">2</div>
          <h3>选择目标</h3>
          <p>配置岗位、行业、面试官风格</p>
        </div>
        <div class="step-arrow">→</div>
        <div class="step">
          <div class="step-number">3</div>
          <h3>备战阶段</h3>
          <p>使用简历优化、自我介绍生成、题库刷题</p>
        </div>
        <div class="step-arrow">→</div>
        <div class="step">
          <div class="step-number">4</div>
          <h3>实战演练</h3>
          <p>进行全真语音/文字模拟面试</p>
        </div>
        <div class="step-arrow">→</div>
        <div class="step">
          <div class="step-number">5</div>
          <h3>复盘提升</h3>
          <p>查看智能评分报告，针对性改进</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.hero-section {
  background: linear-gradient(135deg, var(--color-primary) 0%, #764ba2 100%);
  color: white;
  padding: 100px 0;
  text-align: center;
  border-radius: 10px;
  margin: 20px 0;
}

.hero-content h1 {
  font-size: var(--font-size-h1);
  margin-bottom: 20px;
}

.hero-content p {
  font-size: 1.1rem;
  margin-bottom: 40px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 15px 30px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 1.1rem;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: bold;
}

.primary-btn {
  background-color: var(--color-secondary);
  color: white;
}

.primary-btn:hover {
  background-color: #369f70;
  transform: translateY(-2px);
}

.secondary-btn {
  background-color: transparent;
  color: white;
  border: 2px solid white;
}

.secondary-btn:hover {
  background-color: white;
  color: #667eea;
  transform: translateY(-2px);
}

.features-section {
  padding: 60px 0;
  text-align: center;
}

.features-section h2 {
  font-size: var(--font-size-h2);
  margin-bottom: 50px;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.feature-card {
  background-color: white;
  padding: 32px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  border-radius: 50%;
  background-size: 50%;
  background-position: center;
  background-repeat: no-repeat;
}

.resume-icon {
  background-color: #667eea;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>');
}

.intro-icon {
  background-color: #42b883;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>');
}

.bank-icon {
  background-color: #f093fb;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>');
}

.mock-icon {
  background-color: #4facfe;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 1c-4.96 0-9 4.04-9 9v7c0 1.66 1.34 3 3 3h3v-8H5v-2c0-3.87 3.13-7 7-7s7 3.13 7 7v2h-4v8h3c1.66 0 3-1.34 3-3v-7c0-4.96-4.04-9-9-9z"/></svg>');
}

.strategy-icon {
  background-color: #fa709a;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>');
}

.feature-card h3 {
  font-size: var(--font-size-h3);
  margin-bottom: 15px;
  color: #333;
}

.feature-card p {
  color: #666;
  margin-bottom: 20px;
}

.learn-more {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.learn-more:hover {
  color: var(--color-primary-strong);
  text-decoration: underline;
}

.process-section {
  padding: 60px 0;
  text-align: center;
  background-color: #f8f9fa;
  border-radius: 10px;
  margin: 20px 0;
}

.process-section h2 {
  font-size: var(--font-size-h2);
  margin-bottom: 50px;
  color: #333;
}

.process-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.step {
  background-color: white;
  padding: 24px 16px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 150px;
  position: relative;
}

.step-number {
  width: 44px;
  height: 44px;
  background-color: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 15px;
}

.step h3 {
  font-size: 1.1rem;
  margin-bottom: 10px;
  color: #333;
}

.step p {
  color: #666;
  font-size: 0.9rem;
}

.step-arrow {
  font-size: 2rem;
  color: #667eea;
  font-weight: bold;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: var(--font-size-h1);
  }
  
  .hero-content p {
    font-size: 0.95rem;
  }
  
  .features-section h2,
  .process-section h2 {
    font-size: var(--font-size-h2);
  }
  
  .process-steps {
    flex-direction: column;
  }
  
  .step-arrow {
    transform: rotate(90deg);
  }
}
</style>
