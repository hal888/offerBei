<template>
  <div class="faq-container">
    <div class="faq-header">
      <h1>{{ t('faq.title') }}</h1>
      <p class="subtitle">{{ t('faq.subtitle') }}</p>
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
                <router-link v-if="item.link" :to="item.link" class="faq-link">{{ t('faq.tryNow') }} &rarr;</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="cta-section">
      <h2>{{ t('faq.cta.title') }}</h2>
      <p>{{ t('faq.cta.subtitle') }}</p>
      <router-link to="/register" class="cta-btn">{{ t('faq.cta.btn') }}</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const activeCategory = ref('all')
const openItems = ref({}) // key: groupId-questionIndex

const categories = computed(() => [
  { id: 'all', name: t('faq.categories.all') },
  { id: 'product', name: t('faq.categories.product') },
  { id: 'guide', name: t('faq.categories.guide') },
  { id: 'scenario', name: t('faq.categories.scenario') },
  { id: 'comparison', name: t('faq.categories.comparison') }
])

const faqData = computed(() => [
  {
    id: 'product',
    name: t('faq.groupTitles.product'),
    questions: [
      {
        q: t('faq.questions.product.whatIs.q'),
        a: t('faq.questions.product.whatIs.a'),
        link: '/manual'
      },
      {
        q: t('faq.questions.product.pricing.q'),
        a: t('faq.questions.product.pricing.a'),
        link: '/register'
      },
      {
        q: t('faq.questions.product.security.q'),
        a: t('faq.questions.product.security.a')
      }
    ]
  },
  {
    id: 'guide',
    name: t('faq.groupTitles.guide'),
    questions: [
      {
        q: t('faq.questions.guide.mock.q'),
        a: t('faq.questions.guide.mock.a'),
        link: '/manual#mock'
      },
      {
        q: t('faq.questions.guide.optimize.q'),
        a: t('faq.questions.guide.optimize.a')
      }
    ]
  },
   {
    id: 'scenario',
    name: t('faq.groupTitles.scenario'),
    questions: [
      {
        q: t('faq.questions.scenario.fresher.q'),
        a: t('faq.questions.scenario.fresher.a'),
        link: '/mock-interview'
      },
      {
        q: t('faq.questions.scenario.tech.q'),
        a: t('faq.questions.scenario.tech.a'),
        link: '/question-bank'
      },
      {
        q: t('faq.questions.scenario.bq.q'),
        a: t('faq.questions.scenario.bq.a')
      }
    ]
  },
  {
    id: 'comparison',
    name: t('faq.groupTitles.comparison'),
    questions: [
      {
        q: t('faq.questions.comparison.advantage.q'),
        a: t('faq.questions.comparison.advantage.a')
      },
      {
        q: t('faq.questions.comparison.techFit.q'),
        a: t('faq.questions.comparison.techFit.a')
      }
    ]
  }
])

const filteredGroups = computed(() => {
  if (activeCategory.value === 'all') {
    return faqData.value
  }
  return faqData.value.filter(group => group.id === activeCategory.value)
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
