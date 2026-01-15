<template>
  <div class="manual-container">
    <div class="manual-header">
      <h1>{{ t('manual.title') }}</h1>
      <p class="subtitle">{{ t('manual.subtitle') }}</p>
    </div>

    <div class="manual-content">
      <nav class="manual-nav">
        <ul>
          <li><a href="#resume" :class="{ active: activeSection === 'resume' }" @click.prevent="scrollTo('resume')">{{ t('manual.nav.resume') }}</a></li>
          <li><a href="#intro" :class="{ active: activeSection === 'intro' }" @click.prevent="scrollTo('intro')">{{ t('manual.nav.intro') }}</a></li>
          <li><a href="#questions" :class="{ active: activeSection === 'questions' }" @click.prevent="scrollTo('questions')">{{ t('manual.nav.questions') }}</a></li>
          <li><a href="#mock" :class="{ active: activeSection === 'mock' }" @click.prevent="scrollTo('mock')">{{ t('manual.nav.mock') }}</a></li>
          <li><a href="#strategy" :class="{ active: activeSection === 'strategy' }" @click.prevent="scrollTo('strategy')">{{ t('manual.nav.strategy') }}</a></li>
        </ul>
      </nav>

      <div class="manual-sections">
        <section id="resume" class="manual-section">
          <h2>{{ t('manual.sections.resume.title') }}</h2>
          <div class="section-content">
            <p>{{ t('manual.sections.resume.desc') }}</p>
            <div class="step-list">
              <div class="step-item">
                <span class="step-num">01</span>
                <div class="step-text">
                  <h4>{{ t('manual.sections.resume.steps.upload.title') }}</h4>
                  <p>{{ t('manual.sections.resume.steps.upload.desc') }}</p>
                </div>
              </div>
              <div class="step-item">
                <span class="step-num">02</span>
                <div class="step-text">
                  <h4>{{ t('manual.sections.resume.steps.diagnosis.title') }}</h4>
                  <p>{{ t('manual.sections.resume.steps.diagnosis.desc') }}</p>
                </div>
              </div>
              <div class="step-item">
                <span class="step-num">03</span>
                <div class="step-text">
                  <h4>{{ t('manual.sections.resume.steps.optimize.title') }}</h4>
                  <p>{{ t('manual.sections.resume.steps.optimize.desc') }}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="intro" class="manual-section">
          <h2>{{ t('manual.sections.intro.title') }}</h2>
          <div class="section-content">
            <p>{{ t('manual.sections.intro.desc') }}</p>
            <ul class="feature-list">
              <li><strong>{{ t('manual.sections.intro.features.multiVersion').split('：')[0] || t('manual.sections.intro.features.multiVersion').split(':')[0] }}</strong>: {{ t('manual.sections.intro.features.multiVersion').split('：')[1] || t('manual.sections.intro.features.multiVersion').split(':')[1] }}</li>
              <li><strong>{{ t('manual.sections.intro.features.style').split('：')[0] || t('manual.sections.intro.features.style').split(':')[0] }}</strong>: {{ t('manual.sections.intro.features.style').split('：')[1] || t('manual.sections.intro.features.style').split(':')[1] }}</li>
              <li><strong>{{ t('manual.sections.intro.features.teleprompter').split('：')[0] || t('manual.sections.intro.features.teleprompter').split(':')[0] }}</strong>: {{ t('manual.sections.intro.features.teleprompter').split('：')[1] || t('manual.sections.intro.features.teleprompter').split(':')[1] }}</li>
            </ul>
          </div>
        </section>

        <section id="questions" class="manual-section">
          <h2>{{ t('manual.sections.questions.title') }}</h2>
          <div class="section-content">
            <p>{{ t('manual.sections.questions.desc') }}</p>
            <p>{{ t('manual.sections.questions.desc2') }}</p>
            <div class="question-types">
              <div class="type-badge">{{ t('manual.sections.questions.types.bagu') }}</div>
              <div class="type-badge">{{ t('manual.sections.questions.types.scenario') }}</div>
              <div class="type-badge">{{ t('manual.sections.questions.types.algo') }}</div>
              <div class="type-badge">{{ t('manual.sections.questions.types.bq') }}</div>
            </div>
            <p class="tip">{{ t('manual.sections.questions.tip') }}</p>
          </div>
        </section>

        <section id="mock" class="manual-section">
          <h2>{{ t('manual.sections.mock.title') }}</h2>
          <div class="section-content">
            <p>{{ t('manual.sections.mock.desc') }}</p>
            <div class="step-list">
              <div class="step-item">
                <span class="step-num">01</span>
                <div class="step-text">
                  <h4>{{ t('manual.sections.mock.steps.config.title') }}</h4>
                  <p>{{ t('manual.sections.mock.steps.config.desc') }}</p>
                </div>
              </div>
              <div class="step-item">
                <span class="step-num">02</span>
                <div class="step-text">
                  <h4>{{ t('manual.sections.mock.steps.interact.title') }}</h4>
                  <p>{{ t('manual.sections.mock.steps.interact.desc') }}</p>
                </div>
              </div>
              <div class="step-item">
                <span class="step-num">03</span>
                <div class="step-text">
                  <h4>{{ t('manual.sections.mock.steps.report.title') }}</h4>
                  <p>{{ t('manual.sections.mock.steps.report.desc') }}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="strategy" class="manual-section">
          <h2>{{ t('manual.sections.strategy.title') }}</h2>
          <div class="section-content">
            <p>{{ t('manual.sections.strategy.desc') }}</p>
            <p>{{ t('manual.sections.strategy.desc2') }}</p>
            <ul>
              <li><strong>{{ t('manual.sections.strategy.items.salary').split('：')[0] || t('manual.sections.strategy.items.salary').split(':')[0] }}</strong>: {{ t('manual.sections.strategy.items.salary').split('：')[1] || t('manual.sections.strategy.items.salary').split(':')[1] }}</li>
              <li><strong>{{ t('manual.sections.strategy.items.reverse').split('：')[0] || t('manual.sections.strategy.items.reverse').split(':')[0] }}</strong>: {{ t('manual.sections.strategy.items.reverse').split('：')[1] || t('manual.sections.strategy.items.reverse').split(':')[1] }}</li>
              <li><strong>{{ t('manual.sections.strategy.items.trap').split('：')[0] || t('manual.sections.strategy.items.trap').split(':')[0] }}</strong>: {{ t('manual.sections.strategy.items.trap').split('：')[1] || t('manual.sections.strategy.items.trap').split(':')[1] }}</li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
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
