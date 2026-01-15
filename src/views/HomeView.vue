<template>
  <div class="home-container">
    <header class="hero-section">
      <div class="hero-content">
        <div class="hero-badge">{{ t('home.hero.badge') }}</div>
        <h1>{{ t('home.hero.title') }}</h1>
        <p>{{ t('home.hero.subtitle') }}</p>
        <div class="cta-buttons">
          <router-link to="/resume" class="btn primary-btn" @click="trackEvent('home_cta_click', { button: 'start_now' })">{{ t('home.hero.startBtn') }}</router-link>
          <router-link to="/manual" class="btn secondary-btn" @click="trackEvent('home_cta_click', { button: 'manual' })">{{ t('home.hero.manualBtn') }}</router-link>
        </div>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-num">1000+</span>
            <span class="stat-label">{{ t('home.hero.stats.experiences') }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">98%</span>
            <span class="stat-label">{{ t('home.hero.stats.rating') }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">24h</span>
            <span class="stat-label">{{ t('home.hero.stats.availability') }}</span>
          </div>
        </div>
      </div>
    </header>

    <section class="features-section">
      <h2>{{ t('home.features.title') }}</h2>
      <p class="section-desc">{{ t('home.features.subtitle') }}</p>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon resume-icon"></div>
          <h3>{{ t('home.features.resume.title') }}</h3>
          <p>{{ t('home.features.resume.desc') }}</p>
          <router-link to="/resume" class="learn-more">{{ t('home.features.resume.action') }} &rarr;</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon intro-icon"></div>
          <h3>{{ t('home.features.intro.title') }}</h3>
          <p>{{ t('home.features.intro.desc') }}</p>
          <router-link to="/self-intro" class="learn-more">{{ t('home.features.intro.action') }} &rarr;</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon bank-icon"></div>
          <h3>{{ t('home.features.bank.title') }}</h3>
          <p>{{ t('home.features.bank.desc') }}</p>
          <router-link to="/question-bank" class="learn-more">{{ t('home.features.bank.action') }} &rarr;</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon mock-icon"></div>
          <h3>{{ t('home.features.mock.title') }}</h3>
          <p>{{ t('home.features.mock.desc') }}</p>
          <router-link to="/mock-interview" class="learn-more">{{ t('home.features.mock.action') }} &rarr;</router-link>
        </div>

        <div class="feature-card">
          <div class="feature-icon strategy-icon"></div>
          <h3>{{ t('home.features.strategy.title') }}</h3>
          <p>{{ t('home.features.strategy.desc') }}</p>
          <router-link to="/strategy" class="learn-more">{{ t('home.features.strategy.action') }} &rarr;</router-link>
        </div>
      </div>
    </section>

    <section class="roles-section">
      <div class="roles-container">
        <div class="roles-image">
          <img src="/diverse_roles.png" alt="全行业覆盖，海量题库" />
        </div>
        <div class="roles-content">
          <h2>{{ t('home.roles.title') }}</h2>
          <p class="roles-subtitle">{{ t('home.roles.subtitle') }}</p>
          <div class="roles-tags">
            <span class="role-tag">{{ t('home.roles.tags.internet') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.finance') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.education') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.ecommerce') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.media') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.medical') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.dev') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.pm') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.ops') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.design') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.sales') }}</span>
            <span class="role-tag">{{ t('home.roles.tags.hr') }}</span>
          </div>
          <p class="roles-desc">
            {{ t('home.roles.desc') }}
          </p>
          <router-link to="/question-bank" class="btn primary-btn small-btn">{{ t('home.roles.action') }}</router-link>
        </div>
      </div>
    </section>

    <section class="testimonials-section">
      <h2>{{ t('home.testimonials.title') }}</h2>
      <p class="section-desc">{{ t('home.testimonials.subtitle') }}</p>
      
      <div class="testimonials-grid">
        <div 
          v-for="(item, index) in testimonialList" 
          :key="index" 
          class="testimonial-card"
        >
          <div class="card-header">
            <img :src="item.avatar" alt="User Avatar" class="user-avatar" />
            <div class="user-info">
              <h4>{{ t(`home.testimonials.items[${index}].name`) }}</h4>
              <p>{{ t(`home.testimonials.items[${index}].role`) }}</p>
            </div>
            <div class="rating">⭐⭐⭐⭐⭐</div>
          </div>
          <p class="card-text">"{{ t(`home.testimonials.items[${index}].text`) }}"</p>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { trackEvent } from '@/utils/analytics'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Testimonial avatars mapping
const testimonialList = [
  { avatar: '/avatar_1.png' },
  { avatar: '/avatar_2_real_cn.png' },
  { avatar: '/avatar_3_real_cn.png' },
  { avatar: '/avatar_4_scenery.png' },
  { avatar: '/avatar_5_anime.png' },
  { avatar: '/avatar_6_real_cn.png' }
]
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
