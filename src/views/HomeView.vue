<template>
  <div class="home-container">
    <header class="hero-section">
      <div class="hero-content">
        <div class="hero-badge">AI 驱动的面试神器</div>
        <h1>Offer贝，助你轻松拿Offer</h1>
        <p>一站式解决求职痛点：简历优化、自我介绍生成、智能题库、模拟面试。让每一次面试都自信满满。</p>
        <div class="cta-buttons">
          <router-link to="/resume" class="btn primary-btn" @click="trackEvent('home_cta_click', { button: 'start_now' })">立即开始免费使用</router-link>
          <router-link to="/manual" class="btn secondary-btn" @click="trackEvent('home_cta_click', { button: 'manual' })">使用手册</router-link>
        </div>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-num">1000+</span>
            <span class="stat-label">真实面经</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">98%</span>
            <span class="stat-label">好评率</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">24h</span>
            <span class="stat-label">随时待命</span>
          </div>
        </div>
      </div>
    </header>

    <section class="features-section">
      <h2>核心功能</h2>
      <p class="section-desc">全流程 AI 辅助，从简历到面试，不仅是工具，更是你的私人求职教练</p>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon resume-icon"></div>
          <h3>简历解析与智能优化</h3>
          <p>基于 AI 深度分析，自动识别简历结构，提供 STAR 法则重写建议，精准注入高频关键词，让你的简历脱颖而出。</p>
          <router-link to="/resume" class="learn-more">去优化简历 &rarr;</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon intro-icon"></div>
          <h3>定制化自我介绍</h3>
          <p>针对不同面试场景，生成 30秒/3分钟/5分钟 多版本自我介绍。支持口语化润色，提供提词器模式，告别忘词尴尬。</p>
          <router-link to="/self-intro" class="learn-more">生成自我介绍 &rarr;</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon bank-icon"></div>
          <h3>智能题库与定向突击</h3>
          <p>覆盖高频必问、深挖追问、专业技能及行为情景题。AI 智能出题，针对性查漏补缺，拒绝盲目刷题。</p>
          <router-link to="/question-bank" class="learn-more">开始刷题 &rarr;</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon mock-icon"></div>
          <h3>全真模拟真人面试</h3>
          <p>支持语音/文字双模式，可选严厉/温和等多种面试官风格。实时语音交互，课后生成详细复盘报告，快速提升实战能力。</p>
          <router-link to="/mock-interview" class="learn-more">开始模拟面试 &rarr;</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon strategy-icon"></div>
          <h3>面试策略锦囊</h3>
          <p>独家面试策略库，提供劣势防御话术、薪资谈判技巧及高质量反问问题，助你掌握面试主动权。</p>
          <router-link to="/strategy" class="learn-more">查看策略 &rarr;</router-link>
        </div>
      </div>
    </section>

    <section class="roles-section">
      <div class="roles-container">
        <div class="roles-image">
          <img src="/diverse_roles.png" alt="全行业覆盖，海量题库" />
        </div>
        <div class="roles-content">
          <h2>全行业覆盖，海量真题库</h2>
          <p class="roles-subtitle">无论你是技术大牛、产品专家，还是职场新人，offer贝提供专业的面试支持</p>
          <div class="roles-tags">
            <span class="role-tag">互联网</span>
            <span class="role-tag">金融</span>
            <span class="role-tag">教育</span>
            <span class="role-tag">电商</span>
            <span class="role-tag">传媒</span>
            <span class="role-tag">医疗</span>
            <span class="role-tag">软件开发</span>
            <span class="role-tag">产品经理</span>
            <span class="role-tag">运营</span>
            <span class="role-tag">设计</span>
            <span class="role-tag">销售</span>
            <span class="role-tag">HR</span>
          </div>
          <p class="roles-desc">
            收录全网最新面经，覆盖 100+ 行业，500+ 岗位。针对不同职级定制专属题库，从校招基础到专家深挖，助你从容应对各种面试挑战。
          </p>
          <router-link to="/question-bank" class="btn primary-btn small-btn">浏览海量题库</router-link>
        </div>
      </div>
    </section>

    <section class="testimonials-section">
      <h2>offer贝 助力 1K+ 求职者斩获心仪 Offer</h2>
      <p class="section-desc">听听他们怎么说，你的成功也可以复制</p>
      
      <div class="testimonials-grid">
        <!-- User 1: Frontend - ByteDance -->
        <div class="testimonial-card">
          <div class="card-header">
            <img src="/avatar_1.png" alt="User Avatar" class="user-avatar" />
            <div class="user-info">
              <h4>张沐熙</h4>
              <p>字节跳动 · 前端开发</p>
            </div>
            <div class="rating">⭐⭐⭐⭐⭐</div>
          </div>
          <p class="card-text">"模拟面试真的太强了！AI 面试官问的 React 原理和性能优化问题非常有深度，和我实际面试遇到的几乎一模一样。提前演练让我面试时自信了很多。"</p>
        </div>

        <!-- User 2: Product - Tencent -->
        <div class="testimonial-card">
          <div class="card-header">
            <img src="/avatar_2_real_cn.png" alt="User Avatar" class="user-avatar" />
            <div class="user-info">
              <h4>Ruby</h4>
              <p>腾讯 · 产品经理</p>
            </div>
            <div class="rating">⭐⭐⭐⭐⭐</div>
          </div>
          <p class="card-text">"简历优化功能帮了大忙。AI 指出的 STAR 法则应用问题一针见血，修改后的简历通过率明显提升。产品思维题库也很棒，拓宽了我的思路。"</p>
        </div>

        <!-- User 3: Backend - Alibaba -->
        <div class="testimonial-card">
          <div class="card-header">
            <img src="/avatar_3_real_cn.png" alt="User Avatar" class="user-avatar" />
            <div class="user-info">
              <h4>王晓飞</h4>
              <p>阿里巴巴 · Java 后端</p>
            </div>
            <div class="rating">⭐⭐⭐⭐⭐</div>
          </div>
          <p class="card-text">"作为技术人，最怕面试被问倒。offer贝的智能题库覆盖了高并发、微服务等核心考点，高分思路解析让我学会了如何系统化地回答技术难题。"</p>
        </div>

        <!-- User 4: Data Analyst - Meituan -->
        <div class="testimonial-card">
          <div class="card-header">
            <img src="/avatar_4_scenery.png" alt="User Avatar" class="user-avatar" />
            <div class="user-info">
              <h4>Chloe Chen</h4>
              <p>美团 · 数据分析</p>
            </div>
            <div class="rating">⭐⭐⭐⭐⭐</div>
          </div>
          <p class="card-text">"面试策略锦囊里的薪资谈判技巧很实用！让我成功在 Offer 沟通环节争取到了期望的薪资包（涨幅 30%+）。非常感谢 offer贝 的指导！"</p>
        </div>

        <!-- User 5: Operations - Xiaohongshu -->
        <div class="testimonial-card">
          <div class="card-header">
            <img src="/avatar_5_anime.png" alt="User Avatar" class="user-avatar" />
            <div class="user-info">
              <h4>风禾尽起</h4>
              <p>小红书 · 用户运营</p>
            </div>
            <div class="rating">⭐⭐⭐⭐⭐</div>
          </div>
          <p class="card-text">"自我介绍生成器太好用了，针对不同时长的版本都有。提词器功能让我录制视频面试时完全不卡壳，表现非常自然流畅。"</p>
        </div>

        <!-- User 6: Algo - Huawei -->
        <div class="testimonial-card">
          <div class="card-header">
            <img src="/avatar_6_real_cn.png" alt="User Avatar" class="user-avatar" />
            <div class="user-info">
              <h4>赵科瑞</h4>
              <p>华为 · 算法工程师</p>
            </div>
            <div class="rating">⭐⭐⭐⭐⭐</div>
          </div>
          <p class="card-text">"对于算法岗，深挖项目细节是常态。AI 模拟面试能够针对我的项目经历进行多轮追问，帮我理清了逻辑漏洞，实战效果满分。"</p>
        </div>

      </div>
    </section>

  </div>
</template>

<script setup>
import { trackEvent } from '@/utils/analytics'
</script>

<style scoped>
.home-container {
  width: 100%;
  margin: 0;
  padding: 0;
}

.hero-section {
  background: var(--gradient-primary);
  color: white;
  padding: 80px 20px 100px;
  text-align: center;
  border-radius: 0 0 50% 50% / 40px;
  margin: -20px -20px 60px -20px;
  position: relative;
  overflow: hidden;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.hero-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.hero-content h1 {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 24px;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.hero-content p {
  font-size: 1.25rem;
  margin-bottom: 40px;
  opacity: 0.9;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 60px;
}

.btn {
  padding: 16px 32px;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
}

.primary-btn {
  background-color: var(--color-secondary);
  color: white;
  box-shadow: 0 4px 15px rgba(66, 184, 131, 0.4);
}

.primary-btn:hover {
  background-color: #3aa876;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(66, 184, 131, 0.5);
}

.secondary-btn {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
}

.secondary-btn:hover {
  background-color: white;
  color: var(--color-primary);
  transform: translateY(-2px);
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 40px;
  padding-top: 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-num {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.section-desc {
  text-align: center;
  max-width: 600px;
  margin: 0 auto 50px;
  color: var(--color-text-light);
  font-size: 1.1rem;
}

.features-section {
  padding: 40px 0 80px;
  text-align: center;
}

.features-section h2,
.process-section h2,
.faq-section h2 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: var(--color-text);
  font-weight: 700;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background-color: white;
  padding: 40px 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid var(--color-border);
  text-align: left;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 24px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.resume-icon { background: #e0e7ff; color: #4338ca; }
.intro-icon { background: #dcfce7; color: #15803d; }
.bank-icon { background: #fae8ff; color: #a21caf; }
.mock-icon { background: #e0f2fe; color: #0369a1; }
.strategy-icon { background: #ffe4e6; color: #be123c; }

/* Placeholder icons - ideally use SVG components or library */
.feature-icon::before { content: ''; display: block; width: 32px; height: 32px; background-size: contain; background-repeat: no-repeat; }
.resume-icon::before { background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="%23667eea"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>'); }
.intro-icon::before { background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="%2342b883"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" /></svg>'); }
.bank-icon::before { background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="%23a21caf"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>'); }
.mock-icon::before { background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="%230369a1"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" /></svg>'); }
.strategy-icon::before { background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="%23be123c"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>'); }


.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 12px;
  color: var(--color-text);
  font-weight: 700;
}

.feature-card p {
  color: var(--color-text-light);
  margin-bottom: 24px;
  line-height: 1.6;
}

.learn-more {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  transition: color 0.2s;
}

.learn-more:hover {
  color: var(--color-primary-strong);
}

.process-section {
  padding: 80px 0;
  text-align: center;
  background-color: transparent;
  margin: 40px 0;
}

.process-steps {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 30px;
  margin-top: 50px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 20px;
}

.step {
  background-color: white;
  padding: 30px 20px;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  width: 220px;
  position: relative;
  transition: transform 0.3s;
}

.step:hover {
  transform: translateY(-5px);
}

.step-number {
  width: 50px;
  height: 50px;
  background: var(--gradient-primary);
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 20px;
  box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
}

.step h3 {
  font-size: 1.25rem;
  margin-bottom: 10px;
  color: var(--color-text);
}

.step p {
  color: var(--color-text-light);
  font-size: 0.95rem;
}

.step-arrow {
  font-size: 2rem;
  color: var(--color-primary);
  font-weight: 300;
  margin-top: 60px;
}

.faq-section {
  padding: 60px 0 100px;
  text-align: center;
}

.faq-grid {
  max-width: 900px;
  margin: 0 auto;
  display: grid;
  gap: 20px;
  text-align: left;
  padding: 0 20px;
}

.faq-item {
  background: white;
  padding: 30px;
  border-radius: 16px;
  border: 1px solid var(--color-border);
}

.faq-item h3 {
  font-size: 1.2rem;
  color: var(--color-text);
  margin-bottom: 15px;
  font-weight: 600;
}

.faq-item p {
  color: var(--color-text-light);
  line-height: 1.6;
}


.roles-section {
  padding: 80px 0;
  background-color: #f8fafc;
}

.roles-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 60px;
  padding: 0 20px;
}

.roles-image {
  flex: 1;
}

.roles-image img {
  width: 100%;
  max-width: 550px;
  height: auto;
  border-radius: 20px;
  /* box-shadow: 0 20px 40px rgba(0,0,0,0.1); Optional: if image needs it */
}

.roles-content {
  flex: 1;
  text-align: left;
}

.roles-content h2 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: var(--color-text);
  font-weight: 700;
}

.roles-subtitle {
  font-size: 1.25rem;
  color: var(--color-text);
  margin-bottom: 30px;
  line-height: 1.5;
  font-weight: 500;
}

.roles-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 30px;
}

.role-tag {
  background: white;
  padding: 8px 18px;
  border-radius: 50px;
  font-size: 0.95rem;
  color: var(--color-primary);
  border: 1px solid rgba(66, 184, 131, 0.3);
  font-weight: 500;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}

.roles-desc {
  margin-bottom: 30px;
  color: var(--color-text-light);
  line-height: 1.8;
  font-size: 1.05rem;
}

.small-btn {
  padding: 12px 30px;
  font-size: 1.05rem;
}


.testimonials-section {
  padding: 80px 0 100px;
  background-color: white;
  text-align: center;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 50px auto 0;
  padding: 0 20px;
}

.testimonial-card {
  background: #f8fafc;
  padding: 30px;
  border-radius: 20px;
  text-align: left;
  border: 1px solid var(--color-border);
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  background: white;
  border-color: var(--color-primary);
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 15px;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.user-info h4 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 4px;
}

.user-info p {
  font-size: 0.9rem;
  color: var(--color-text-light);
  margin: 0;
}

.rating {
  margin-left: auto;
  font-size: 0.9rem;
  letter-spacing: -2px;
}

.card-text {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--color-text);
  font-style: italic;
  opacity: 0.9;
}

@media (max-width: 768px) {

  .roles-container {
    flex-direction: column;
    text-align: center;
    gap: 40px;
  }
  
  .roles-content {
    text-align: center;
    order: 2;
  }

  .roles-image {
    order: 1;
  }
  
  .roles-tags {
    justify-content: center;
  }

  .hero-section {
    padding: 60px 20px 80px;
    border-radius: 0 0 30px 30px;
  }
  
  .hero-content h1 {
    font-size: 2.25rem;
  }
  
  .hero-stats {
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .process-steps {
    flex-direction: column;
    align-items: center;
  }
  
  .step-arrow {
    transform: rotate(90deg);
    margin: 10px 0;
  }
  
  .step {
    width: 100%;
    max-width: 300px;
  }

  .testimonials-grid {
    grid-template-columns: 1fr;
    padding: 0;
  }
}
</style>
