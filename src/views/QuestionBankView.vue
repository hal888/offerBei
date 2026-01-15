<template>
  <div class="question-bank-container">
    <h1>{{ $t('pages.questionBank.title') }}</h1>
    
    <!-- 生成题库遮盖层 -->
    <div v-if="isGenerating" class="generate-overlay">
      <div class="generate-loading">
        <div class="loading-spinner"></div>
        <h3>{{ $t('loading.generatingBank') }}</h3>
        <p>{{ $t('loading.generatingBankDesc') }}</p>
      </div>
    </div>
    
    <div class="question-config-section">
      <div class="config-card">
        <h2>{{ $t('pages.questionBank.desc') }}</h2>
        
        <div class="config-options">
          <div class="option-group">
            <label>{{ $t('pages.questionBank.count.label') }}</label>
            <div class="option-buttons">
              <button 
                v-for="count in questionCounts" 
                :key="count" 
                :class="['option-btn', { active: selectedCount === count }]" 
                @click="selectedCount = count"
              >
                {{ count }}{{ $t('pages.questionBank.count.suffix') }}
              </button>
            </div>
            <p class="option-desc">{{ getCountDescription(selectedCount) }}</p>
          </div>

          <div class="option-group">
            <label>{{ $t('pages.questionBank.typeDistribution') }}</label>
            <div class="question-types">
              <div class="type-item">
                <span class="type-label">{{ $t('pages.questionBank.types.highFreq') }}</span>
                <span class="type-percentage">30%</span>
              </div>
              <div class="type-item">
                <span class="type-label">{{ $t('pages.questionBank.types.deepDive') }}</span>
                <span class="type-percentage">25%</span>
              </div>
              <div class="type-item">
                <span class="type-label">{{ $t('pages.questionBank.types.technical') }}</span>
                <span class="type-percentage">25%</span>
              </div>
              <div class="type-item">
                <span class="type-label">{{ $t('pages.questionBank.types.behavioral') }}</span>
                <span class="type-percentage">20%</span>
              </div>
            </div>
          </div>

          <div class="option-group">
            <label>{{ $t('pages.questionBank.topic.label') }}</label>
            <input 
              type="text" 
              v-model="customTopic" 
              :placeholder="$t('pages.questionBank.topic.placeholder')"
              :disabled="isGenerating"
            />
            <p class="option-desc">{{ $t('pages.questionBank.topic.desc') }}</p>
          </div>

          <button 
            class="generate-btn" 
            @click="generateQuestions"
            :disabled="isGenerating"
          >
            <span class="btn-icon">🎯</span>
            {{ isGenerating ? $t('loading.generatingBank') : $t('pages.questionBank.generate') }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="questions.length > 0" class="questions-section">
      <h2>{{ $t('pages.questionBank.resultTitle') }}</h2>
      
      <div class="questions-header">
        <div class="questions-info">
          <span class="total-count">{{ questions.length }}{{ $t('pages.questionBank.count.suffix') }}</span>
          <span class="topic-tag" v-if="customTopic">{{ $t('pages.questionBank.topicLabel') }}：{{ customTopic }}</span>
        </div>
        <div class="questions-actions">
          <button class="action-btn" @click="exportQuestions">
            <span class="action-icon">📥</span>
            {{ $t('pages.questionBank.export') }}
          </button>
        </div>
      </div>

      <div class="questions-list">
        <div 
          v-for="(question, index) in questions" 
          :key="index" 
          class="question-item"
        >
          <div class="question-header">
            <div class="question-number">{{ index + 1 }}</div>
            <div class="question-type-badge">{{ question.type }}</div>
          </div>
          <div class="question-content">
            {{ question.content }}
          </div>
          <div class="question-footer">
            <button class="expand-btn" @click="toggleAnswer(index)">
              <span class="expand-icon">{{ question.showAnswer ? '▼' : '▶️' }}</span>
              {{ question.showAnswer ? $t('pages.questionBank.hideAnswer') : $t('pages.questionBank.showAnswer') }}
            </button>
          </div>
          
          <div v-if="question.showAnswer" class="answer-section">
            <div class="answer-header">
              <h4>{{ $t('pages.questionBank.answerTitle') }}</h4>
            </div>
            <div class="answer-content">
              {{ question.answer }}
            </div>
            <div class="answer-analysis">
              <h5>{{ $t('pages.questionBank.interviewerIntent') }}</h5>
              <p>{{ question.analysis }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- 错误提示组件 -->
  <ErrorMessage 
    :show="showError" 
    :message="errorMessage" 
    :title="errorTitle"
    @close="closeError"
  />
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import apiClient from '@/utils/api.js'
import ErrorMessage from '@/components/ErrorMessage.vue'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import { trackEvent } from '@/utils/analytics'

const router = useRouter()
const { t } = useI18n()

// 错误提示相关
const showError = ref(false)
const errorMessage = ref('')
const errorTitle = ref('提示')
// 错误提示关闭后的回调函数
const errorCloseCallback = ref(null)

// 显示错误信息
const showErrorMessage = (message, title = t('alerts.title'), callback = null) => {
  errorMessage.value = message
  errorTitle.value = title
  errorCloseCallback.value = callback
  showError.value = true
}

// 关闭错误信息
const closeError = () => {
  showError.value = false
  errorMessage.value = ''
  errorTitle.value = t('alerts.title')
  // 执行回调函数
  if (errorCloseCallback.value) {
    const callback = errorCloseCallback.value
    errorCloseCallback.value = null
    callback()
  }
}

const selectedCount = ref(10)
const customTopic = ref('')
const questions = ref([])
const isGenerating = ref(false)

// 页面加载时自动获取已生成的题库数据
onMounted(async () => {
  // 验证selectedCount是否在允许范围内，如果是100则重置为50
  const allowedCounts = [10, 30, 50]
  if (!allowedCounts.includes(selectedCount.value)) {
    console.warn(`[WARNING] selectedCount=${selectedCount.value}不在允许范围内，重置为50`)
    selectedCount.value = 50
  }
  try {
    // 从localStorage获取userId
    const userId = localStorage.getItem('userId')
    
    // 如果没有userId，不自动加载数据（等待用户第一次生成）
    if (!userId) return
    
    // 调用后端API获取已生成的题库数据（不阻塞页面渲染）
    fetchQuestionBank()  // 移除await，让请求在后台进行，不阻塞页面加载
  } catch (error) {
    console.log('获取已生成题库失败:', error)
    // 忽略错误，等待用户手动生成
  }
})

// 根据选择的数量获取题库数据
const fetchQuestionBank = async () => {
  try {
    // 从localStorage获取userId
    const userId = localStorage.getItem('userId')
    
    // 如果没有userId，不获取数据
    if (!userId) return
    
    // 调用后端API获取已生成的题库数据，不传递resumeId参数
    const response = await apiClient.post('/question-bank/get', {
      userId: userId,
      count: selectedCount.value  // 传递选择的题目数量
    })
    
    // 如果返回了题库数据，填充到页面上
    if (response.data && response.data.questions && response.data.questions.length > 0) {
      questions.value = response.data.questions.map(q => ({
        ...q,
        showAnswer: false
      }))
    } else {
      // 如果没有找到数据，清空当前显示
      questions.value = []
    }
  } catch (error) {
    console.log('获取已生成题库失败:', error)
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else if (error.response && error.response.data && error.response.data.error === 'User not found') {
      showErrorMessage(t('alerts.uploadResumeFirst'), t('alerts.title'), () => {
        router.push('/resume')
      })
    }
    // 其他错误忽略，等待用户手动生成
  }
}

const questionCounts = [10, 30, 50]

const getCountDescription = (count) => {
  if (count === 10) return t('pages.questionBank.count.desc10')
  if (count === 30) return t('pages.questionBank.count.desc30')
  if (count === 50) return t('pages.questionBank.count.desc50')
  return ''
}

// 监听题目数量变化，自动获取相应数量的题目
watch(selectedCount, () => {
  fetchQuestionBank()
})

const generateQuestions = () => {
  isGenerating.value = true
  
  // 从localStorage获取userId，如果没有则生成一个新的
  let userId = localStorage.getItem('userId')
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    localStorage.setItem('userId', userId)
  }
  
  console.log('[DEBUG] 准备生成题库')
  console.log('[DEBUG] selectedCount.value:', selectedCount.value)
  console.log('[DEBUG] topic:', customTopic.value)
  console.log('[DEBUG] userId:', userId)
  
  // 验证count值是否在允许范围内
  const allowedCounts = [10, 30, 50]
  const countToSend = allowedCounts.includes(selectedCount.value) ? selectedCount.value : 50
  
  if (countToSend !== selectedCount.value) {
    console.error(`[ERROR] selectedCount=${selectedCount.value}不合法，使用默认值50`)
  }
  
  console.log('[DEBUG] 实际发送的count参数:', countToSend)
  
  // 调用后端API，不传递resumeId参数
  apiClient.post('/question-bank/generate', {
    count: countToSend,
    topic: customTopic.value,
    userId: userId
  })
  .then(response => {
    // 添加调试日志
    console.log('[DEBUG] 题库生成成功，收到响应:', response.data)
    console.log('[DEBUG] questions数组:', response.data.questions)
    console.log('[DEBUG] questions数量:', response.data.questions ? response.data.questions.length : 0)
    
    // 格式化问题数据，添加showAnswer字段
  questions.value = response.data.questions.map(q => ({
    ...q,
    showAnswer: false
  }))
    // Track generate questions event
    trackEvent('generate_questions', {
      count: selectedCount.value,
      has_custom_topic: !!customTopic.value
    })

    // 保存userId到localStorage，确保后续请求使用相同的userId
    if (response.data.userId) {
      localStorage.setItem('userId', response.data.userId)
    }
    // 保存resumeId到localStorage（如果后端返回了新的resumeId）
    if (response.data.resumeId) {
      localStorage.setItem('resumeId', response.data.resumeId)
    }
    
    console.log('[DEBUG] 题库已成功加载到页面')
  })
  .catch(error => {
    console.error('[ERROR] 生成题库失败:', error)
    console.error('[ERROR] 错误详情:', error.response)
    console.error('[ERROR] 错误消息:', error.message)
    
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else {
      showErrorMessage(t('alerts.generateBankFailed'), t('alerts.title'))
    }
  })
  .finally(() => {
    isGenerating.value = false
  })
}

const toggleAnswer = (index) => {
  questions.value[index].showAnswer = !questions.value[index].showAnswer
}

const exportQuestions = async () => {
  if (questions.value.length === 0) {
    showErrorMessage(t('alerts.generateBankFirst'), t('alerts.title'))
    return
  }

  try {
    // 创建一个临时容器来渲染所有题目内容
    const tempContainer = document.createElement('div')
    tempContainer.style.position = 'absolute'
    tempContainer.style.top = '-9999px'
    tempContainer.style.left = '-9999px'
    tempContainer.style.width = '800px' // 设置合适的宽度
    tempContainer.style.padding = '40px'
    tempContainer.style.backgroundColor = '#ffffff'
    tempContainer.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    tempContainer.style.color = '#333333'
    tempContainer.style.boxSizing = 'border-box'
    document.body.appendChild(tempContainer)

    // 生成标题和信息
    const title = document.createElement('h1')
    title.textContent = '智能面试题库'
    title.style.textAlign = 'center'
    title.style.marginBottom = '30px'
    title.style.fontSize = '28px'
    title.style.color = '#2c3e50'
    tempContainer.appendChild(title)

    if (customTopic.value) {
      const topicInfo = document.createElement('div')
      topicInfo.textContent = `话题：${customTopic.value}`
      topicInfo.style.textAlign = 'center'
      topicInfo.style.marginBottom = '20px'
      topicInfo.style.color = '#666666'
      topicInfo.style.fontSize = '16px'
      tempContainer.appendChild(topicInfo)
    }

    const stats = document.createElement('div')
    stats.textContent = `共 ${questions.value.length} 道题目`
    stats.style.textAlign = 'center'
    stats.style.marginBottom = '40px'
    stats.style.color = '#666666'
    stats.style.fontSize = '16px'
    tempContainer.appendChild(stats)

    const instructions = document.createElement('div')
    instructions.textContent = '本题库基于您的简历内容生成，涵盖高频必问题、简历深挖题、专业技能题和行为/情景题等类型，可用于面试前的针对性练习。'
    instructions.style.textAlign = 'center'
    instructions.style.color = '#666666'
    instructions.style.marginBottom = '50px'
    instructions.style.lineHeight = '1.6'
    tempContainer.appendChild(instructions)

    // 生成题目列表
    const questionsList = document.createElement('div')
    questionsList.style.display = 'flex'
    questionsList.style.flexDirection = 'column'
    questionsList.style.gap = '30px'
    tempContainer.appendChild(questionsList)

    questions.value.forEach((question, index) => {
      const questionBlock = document.createElement('div')
      questionBlock.style.borderBottom = '1px solid #e0e0e0'
      questionBlock.style.paddingBottom = '20px'
      
      // 题号和类型
      const questionHeader = document.createElement('div')
      questionHeader.style.display = 'flex'
      questionHeader.style.justifyContent = 'space-between'
      questionHeader.style.alignItems = 'center'
      questionHeader.style.marginBottom = '15px'

      const questionNumber = document.createElement('span')
      questionNumber.textContent = `${index + 1}.`
      questionNumber.style.fontWeight = 'bold'
      questionNumber.style.fontSize = '18px'
      questionHeader.appendChild(questionNumber)

      const questionType = document.createElement('span')
      questionType.textContent = question.type
      questionType.style.backgroundColor = '#f0f4ff'
      questionType.style.color = '#667eea'
      questionType.style.padding = '5px 15px'
      questionType.style.borderRadius = '20px'
      questionType.style.fontSize = '12px'
      questionType.style.fontWeight = 'bold'
      questionHeader.appendChild(questionType)

      questionBlock.appendChild(questionHeader)

      // 问题内容
      const questionContent = document.createElement('div')
      questionContent.textContent = question.content
      questionContent.style.fontSize = '16px'
      questionContent.style.lineHeight = '1.8'
      questionContent.style.marginBottom = '20px'
      questionBlock.appendChild(questionContent)

      // 参考答案
      const answerSection = document.createElement('div')
      answerSection.style.marginBottom = '15px'

      const answerLabel = document.createElement('div')
      answerLabel.textContent = '参考答案：'
      answerLabel.style.fontWeight = 'bold'
      answerLabel.style.marginBottom = '10px'
      answerLabel.style.fontSize = '14px'
      answerLabel.style.color = '#333333'
      answerSection.appendChild(answerLabel)

      const answerContent = document.createElement('div')
      answerContent.textContent = question.answer
      answerContent.style.marginLeft = '20px'
      answerContent.style.color = '#555555'
      answerContent.style.fontSize = '14px'
      answerContent.style.lineHeight = '1.6'
      answerSection.appendChild(answerContent)

      questionBlock.appendChild(answerSection)

      // 面试官意图
      const analysisSection = document.createElement('div')

      const analysisLabel = document.createElement('div')
      analysisLabel.textContent = '面试官意图：'
      analysisLabel.style.fontWeight = 'bold'
      analysisLabel.style.marginBottom = '10px'
      analysisLabel.style.fontSize = '14px'
      analysisLabel.style.color = '#333333'
      analysisSection.appendChild(analysisLabel)

      const analysisContent = document.createElement('div')
      analysisContent.textContent = question.analysis
      analysisContent.style.marginLeft = '20px'
      analysisContent.style.color = '#555555'
      analysisContent.style.fontSize = '14px'
      analysisContent.style.lineHeight = '1.6'
      analysisContent.style.marginBottom = '15px'
      analysisSection.appendChild(analysisContent)

      questionBlock.appendChild(analysisSection)

      questionsList.appendChild(questionBlock)
    })

    // 使用html2canvas将临时容器转换为canvas
    const canvas = await html2canvas(tempContainer, {
      scale: 2, // 提高清晰度
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false
    })

    // 计算PDF尺寸
    const imgData = canvas.toDataURL('image/png')
    const imgWidth = 210 // A4宽度，单位mm
    const imgHeight = (canvas.height * imgWidth) / canvas.width

    // 创建PDF
    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    const pageHeight = 297 // A4高度，单位mm
    let heightLeft = imgHeight
    let position = 0

    // 循环添加多页
    while (heightLeft > 0) {
      // 添加图片到当前页
      doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      
      // 更新剩余高度和位置
      heightLeft -= pageHeight
      position -= pageHeight
      
      // 如果还有剩余内容，添加新页
      if (heightLeft > 0) {
        doc.addPage()
      }
    }

    // 保存PDF文件
    doc.save('智能面试题库.pdf')

    // 清理临时容器
    document.body.removeChild(tempContainer)
  } catch (error) {
    console.error('生成PDF失败:', error)
    showErrorMessage(t('alerts.generatePdfFailed'), t('alerts.title'))
  }
}


</script>

<style scoped>
.question-bank-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.question-bank-container h1 {
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.config-card, .question-item {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.config-card h2, .questions-section h2 {
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.config-options {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.option-group label {
  font-weight: bold;
  color: #333;
  font-size: 1.1rem;
}

.option-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.option-btn {
  padding: 15px 30px;
  border: 2px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  font-size: 1.1rem;
  flex: 1;
  min-width: 120px;
}

.option-btn:hover {
  border-color: #667eea;
}

.option-btn.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.option-desc {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.question-types {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.type-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 5px;
}

.type-label {
  font-weight: bold;
  color: #333;
}

.type-percentage {
  color: #667eea;
  font-weight: bold;
}

.option-group input[type="text"] {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.option-group input[type="text"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.generate-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px 40px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: center;
}

.generate-btn:hover {
  background-color: #369f70;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(66, 184, 131, 0.3);
}

.btn-icon {
  font-size: 1.3rem;
}

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
  flex-wrap: wrap;
  gap: 20px;
}

.questions-info {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.total-count {
  font-weight: bold;
  font-size: 1.1rem;
  color: #333;
}

.topic-tag {
  padding: 5px 15px;
  background-color: #667eea;
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

.questions-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.action-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.action-icon {
  font-size: 1.1rem;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-item {
  border-left: 4px solid #667eea;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.question-number {
  width: 30px;
  height: 30px;
  background-color: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 0.9rem;
}

.question-type-badge {
  padding: 5px 15px;
  background-color: #f0f4ff;
  color: #667eea;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}



.question-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
  margin-bottom: 20px;
}

.question-footer {
  display: flex;
  justify-content: flex-end;
}

.expand-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.expand-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.expand-icon {
  font-size: 0.9rem;
}

.answer-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.answer-header {
  margin-bottom: 15px;
}

.answer-header h4 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
  font-weight: bold;
}

.answer-content {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 20px;
  line-height: 1.6;
  color: #333;
}

.answer-analysis {
  background-color: #e8f4f8;
  padding: 20px;
  border-radius: 5px;
}

.answer-analysis h5 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1rem;
  font-weight: bold;
}

.answer-analysis p {
  margin: 0;
  line-height: 1.6;
  color: #666;
}

/* 生成题库遮盖层样式 */
.generate-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.generate-loading {
  text-align: center;
  padding: 40px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 90%;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  margin: 0 auto 20px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.generate-loading h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.generate-loading p {
  color: #666;
  margin: 0;
  font-size: 1rem;
}

/* 禁用状态样式 */
.option-btn:disabled,
.option-group input:disabled,
.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.generate-btn:disabled:hover {
  background-color: #42b883;
  transform: none;
}

@media (max-width: 768px) {
  .question-bank-container {
    padding: 10px;
  }
  
  .question-bank-container h1 {
    font-size: 2rem;
  }
  
  .config-card, .question-item {
    padding: 20px;
  }
  
  .questions-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .questions-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .question-header {
    flex-wrap: wrap;
  }
  
  .generate-loading {
    padding: 30px 20px;
  }
  
  .loading-spinner {
    width: 50px;
    height: 50px;
  }
}
</style>