<template>
  <div class="strategy-container">
    <div class="strategy-header">
      <h1>{{ $t('pages.strategy.title') }}</h1>
      <button 
        class="export-btn" 
        @click="exportStrategy" 
        :disabled="!analysisResult && generatedQuestions.length === 0"
      >
        <span class="btn-icon">📄</span>
        {{ $t('pages.strategy.export') }}
      </button>
    </div>
    
    <!-- 遮盖层 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <h3>{{ loadingMessage }}</h3>
      </div>
    </div>
    
    <div class="export-content" ref="exportContent">
      <div class="strategy-section">
        <div class="strategy-card">
          <h2>{{ $t('pages.strategy.tabs.analysis') }}</h2>
          
          <div class="strategy-content">
            <div v-if="analysisResult" class="analysis-result">
              <h3>{{ $t('pages.strategy.analysis.result') }}</h3>
              <div class="result-content">
                <div class="result-section" v-for="(section, index) in analysisResult.sections" :key="index">
                  <h4>{{ section.title }}</h4>
                  <p>{{ section.content }}</p>
                  <div class="tips-list">
                    <div class="tip-item" v-for="(tip, tipIndex) in section.tips" :key="tipIndex">
                      <span class="tip-icon">💡</span>
                      <span class="tip-text">{{ tip }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="strategy-section">
        <div class="strategy-card">
          <h2>{{ $t('pages.strategy.tabs.questions') }}</h2>
          
          <div class="strategy-content">
            <div v-if="generatedQuestions.length > 0" class="questions-result">
              <h3>{{ $t('pages.strategy.questions.generated') }}</h3>
              <div class="questions-list">
                <div 
                  v-for="(question, index) in generatedQuestions" 
                  :key="index" 
                  class="question-card"
                >
                  <div class="question-number">{{ index + 1 }}</div>
                  <div class="question-content">
                    {{ question.content }}
                  </div>
                  <div class="question-type-tag">{{ question.type }}</div>
                  <div class="question-explanation">
                    <h5>{{ $t('pages.strategy.questions.intent') }}</h5>
                    <p>{{ question.explanation }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 表单内容（不导出） -->
    <div class="form-content">
      <div class="strategy-section">
        <div class="strategy-card">
          <h3>{{ $t('pages.strategy.analysis.title') }}</h3>
          
          <div class="strategy-content">
            <div class="analysis-options">
              <div class="option-group">
                <label>{{ $t('pages.strategy.analysis.backgroundInfo.label') }}</label>
                <textarea 
                  v-model="backgroundInfo" 
                  :placeholder="$t('pages.strategy.analysis.backgroundInfo.placeholder')"
                  rows="5"
                ></textarea>
              </div>

              <div class="option-group">
                <label>{{ $t('pages.strategy.analysis.optimizationDirections.label') }}</label>
                <div class="direction-options">
                  <label class="direction-checkbox">
                    <input type="checkbox" v-model="selectedDirections" value="空窗期分析" />
                    <span class="checkbox-label">{{ $t('pages.strategy.analysis.optimizationDirections.gapPeriod') }}</span>
                  </label>
                  <label class="direction-checkbox">
                    <input type="checkbox" v-model="selectedDirections" value="转行背景" />
                    <span class="checkbox-label">{{ $t('pages.strategy.analysis.optimizationDirections.careerChange') }}</span>
                  </label>
                  <label class="direction-checkbox">
                    <input type="checkbox" v-model="selectedDirections" value="经验不足" />
                    <span class="checkbox-label">{{ $t('pages.strategy.analysis.optimizationDirections.lackOfExperience') }}</span>
                  </label>
                  <label class="direction-checkbox">
                    <input type="checkbox" v-model="selectedDirections" value="防御性话术" />
                    <span class="checkbox-label">{{ $t('pages.strategy.analysis.optimizationDirections.defensiveLanguage') }}</span>
                  </label>
                </div>
              </div>

              <button class="analyze-btn" @click="generateAnalysis">
                <span class="btn-icon">🔍</span>
                {{ $t('pages.strategy.analysis.generateButton') }}
              </button>
            </div>

            <!-- 结果展示部分 -->
            <div v-if="analysisResult" class="analysis-result">
              <h3>{{ $t('pages.strategy.analysis.result') }}</h3>
              <div class="result-content">
                <div class="result-section" v-for="(section, index) in analysisResult.sections" :key="index">
                  <h4>{{ section.title }}</h4>
                  <p>{{ section.content }}</p>
                  <div class="tips-list">
                    <div class="tip-item" v-for="(tip, tipIndex) in section.tips" :key="tipIndex">
                      <span class="tip-icon">💡</span>
                      <span class="tip-text">{{ tip }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="strategy-section">
        <div class="strategy-card">
          <h3>{{ $t('pages.strategy.questions.title') }}</h3>
          
          <div class="strategy-content">
            <div class="question-generation">
              <div class="option-group">
                <label>{{ $t('pages.strategy.questions.companyPosition.label') }}</label>
                <div class="company-inputs">
                  <input 
                    type="text" 
                    v-model="companyInfo.companyName" 
                    :placeholder="$t('pages.strategy.questions.companyPosition.companyNamePlaceholder')"
                    class="company-input"
                  />
                  <input 
                    type="text" 
                    v-model="companyInfo.position" 
                    :placeholder="$t('pages.strategy.questions.companyPosition.positionPlaceholder')"
                    class="company-input"
                  />
                </div>
              </div>

              <div class="option-group">
                <label>{{ $t('pages.strategy.questions.questionTypes.label') }}</label>
                <div class="question-types">
                  <label class="type-checkbox">
                    <input type="checkbox" v-model="selectedQuestionTypes" value="公司发展类" />
                    <span class="checkbox-label">{{ $t('pages.strategy.questions.questionTypes.companyDevelopment') }}</span>
                  </label>
                  <label class="type-checkbox">
                    <input type="checkbox" v-model="selectedQuestionTypes" value="团队文化类" />
                    <span class="checkbox-label">{{ $t('pages.strategy.questions.questionTypes.teamCulture') }}</span>
                  </label>
                  <label class="type-checkbox">
                    <input type="checkbox" v-model="selectedQuestionTypes" value="岗位发展类" />
                    <span class="checkbox-label">{{ $t('pages.strategy.questions.questionTypes.roleResponsibilities') }}</span>
                  </label>
                  <label class="type-checkbox">
                    <span class="checkbox-label">{{ $t('pages.strategy.questions.questionTypes.developmentOpportunities') }}</span>
                  </label>
                </div>
              </div>

              <button class="generate-questions-btn" @click="generateQuestions">
                <span class="btn-icon">✨</span>
                {{ $t('pages.strategy.questions.generateButton') }}
              </button>
            </div>

            <!-- 结果展示部分 -->
            <div v-if="generatedQuestions.length > 0" class="questions-result">
              <h3>{{ $t('pages.strategy.questions.generated') }}</h3>
              <div class="questions-list">
                <div 
                  v-for="(question, index) in generatedQuestions" 
                  :key="index" 
                  class="question-card"
                >
                  <div class="question-number">{{ index + 1 }}</div>
                  <div class="question-content">
                    {{ question.content }}
                  </div>
                  <div class="question-type-tag">{{ question.type }}</div>
                  <div class="question-explanation">
                    <h5>{{ $t('pages.strategy.questions.intent') }}</h5>
                    <p>{{ question.explanation }}</p>
                  </div>
                </div>
              </div>
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
import { ref, onMounted, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import ErrorMessage from '@/components/ErrorMessage.vue'
import apiClient from '@/utils/api.js'
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

const backgroundInfo = ref('')
const selectedDirections = ref([])
const analysisResult = ref(null)
const companyInfo = ref({ companyName: '', position: '' })
const selectedQuestionTypes = ref([])
const generatedQuestions = ref([])
const isAnalyzing = ref(false)
const isGeneratingQuestions = ref(false)
// 添加遮盖层相关变量
const isLoading = ref(false)
const loadingMessage = ref('')
// 添加导出相关变量
const exportContent = ref(null)

const generateAnalysis = () => {
  isAnalyzing.value = true
  isLoading.value = true
  loadingMessage.value = t('loading.generatingAnalysis')
  
  const userId = getUserId()
  
  // 调用后端API
  apiClient.post('/strategy/analysis', {
    backgroundInfo: backgroundInfo.value,
    directions: selectedDirections.value,
    userId: userId
  })
  .then(response => {
    analysisResult.value = response.data
  })
  .catch(error => {
    console.error('生成画像分析失败:', error)
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else if (error.response && error.response.data.error === 'User not found') {
      showErrorMessage(t('alerts.uploadResumeFirst'), t('alerts.title'), () => {
        router.push('/resume')
      })
    } else {
      showErrorMessage(t('alerts.generateAnalysisFailed'), t('alerts.title'))
    }
  })
  .finally(() => {
    isAnalyzing.value = false
    isLoading.value = false
  })
}

const generateQuestions = () => {
  isGeneratingQuestions.value = true
  isLoading.value = true
  loadingMessage.value = t('loading.generatingQuestions')
  
  const userId = getUserId()
  
  // 调用后端API
  apiClient.post('/strategy/questions', {
    companyName: companyInfo.value.companyName,
    position: companyInfo.value.position,
    questionTypes: selectedQuestionTypes.value,
    userId: userId
  })
  .then(response => {
    generatedQuestions.value = response.data.questions
    
    // Track generate questions event
    trackEvent('generate_strategy_questions', {
      company: companyInfo.value.companyName,
      position: companyInfo.value.position,
      types: selectedQuestionTypes.value
    })
  })
  .catch(error => {
    console.error('生成问题失败:', error)
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else if (error.response && error.response.data.error === 'User not found') {
      showErrorMessage(t('alerts.uploadResumeFirst'), t('alerts.title'), () => {
        router.push('/resume')
      })
    } else {
      showErrorMessage(t('alerts.generateQuestionFailed'), t('alerts.title'))
    }
  })
  .finally(() => {
    isGeneratingQuestions.value = false
    isLoading.value = false
  })
}

// 获取userId的辅助函数
const getUserId = () => {
  let userId = localStorage.getItem('userId')
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    localStorage.setItem('userId', userId)
  }
  return userId
}

// 获取已有的画像分析历史
const fetchAnalysisHistory = async () => {
  const userId = getUserId()
  
  try {
    const response = await apiClient.get(`/strategy/analysis/history`)
    if (response.data && response.data.length > 0) {
      // 使用最新的分析结果
      analysisResult.value = response.data[0].result
    } else {
      // 如果没有历史记录，清空当前数据
      analysisResult.value = null
    }
  } catch (error) {
    console.error('获取画像分析历史失败:', error)
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else if (error.response && error.response.data.error === 'User not found') {
      showErrorMessage(t('alerts.uploadResumeFirst'), t('alerts.title'), () => {
        router.push('/resume')
      })
    }
    // 其他错误时也清空数据
    analysisResult.value = null
  }
}

// 获取已有的反问问题历史
const fetchQuestionsHistory = async () => {
  const userId = getUserId()
  
  try {
    const response = await apiClient.get(`/strategy/questions/history`)
    if (response.data && response.data.length > 0) {
      // 使用最新的问题结果
      generatedQuestions.value = response.data[0].result.questions || []
      // 恢复公司信息
      companyInfo.value.companyName = response.data[0].company_name || ''
      companyInfo.value.position = response.data[0].position || ''
    } else {
      // 如果没有历史记录，清空当前数据
      generatedQuestions.value = []
      companyInfo.value.companyName = ''
      companyInfo.value.position = ''
    }
  } catch (error) {
    console.error('获取反问问题历史失败:', error)
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else if (error.response && error.response.data.error === 'User not found') {
      showErrorMessage(t('alerts.uploadResumeFirst'), t('alerts.title'), () => {
        router.push('/resume')
      })
    }
    // 其他错误时也清空数据
    generatedQuestions.value = []
    companyInfo.value.companyName = ''
    companyInfo.value.position = ''
  }
}

// 统一加载历史数据的函数
const loadHistoryData = async () => {
  // 同时获取画像分析历史和反问问题历史
  await Promise.all([
    fetchAnalysisHistory(),
    fetchQuestionsHistory()
  ])
}

// 页面加载时自动获取已有的面试策略内容
onMounted(async () => {
  await loadHistoryData()
})

// 每次组件激活时（包括从其他路由返回时）都重新加载数据
onActivated(async () => {
  await loadHistoryData()
})

const exportStrategy = async () => {
  try {
    isLoading.value = true
    loadingMessage.value = t('loading.generatingPdf')
    
    // 准备导出内容容器
    const tempExportContainer = document.createElement('div')
    tempExportContainer.className = 'temp-export-container'
    tempExportContainer.style.position = 'absolute'
    tempExportContainer.style.left = '-9999px'
    tempExportContainer.style.top = '-9999px'
    tempExportContainer.style.width = '800px'
    tempExportContainer.style.backgroundColor = '#ffffff'
    tempExportContainer.style.padding = '20px'
    tempExportContainer.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)'
    
    // 添加标题
    const title = document.createElement('h1')
    title.textContent = '面试策略锦囊'
    title.style.textAlign = 'center'
    title.style.marginBottom = '30px'
    title.style.color = '#333'
    tempExportContainer.appendChild(title)
    
    // 添加画像分析结果（如果有）
    if (analysisResult.value) {
      const analysisSection = document.createElement('div')
      analysisSection.className = 'strategy-section'
      
      const analysisCard = document.createElement('div')
      analysisCard.className = 'strategy-card'
      analysisCard.style.marginBottom = '30px'
      
      const analysisTitle = document.createElement('h2')
      analysisTitle.textContent = '画像分析'
      analysisTitle.style.textAlign = 'center'
      analysisTitle.style.paddingBottom = '20px'
      analysisTitle.style.borderBottom = '2px solid #f0f0f0'
      analysisCard.appendChild(analysisTitle)
      
      const analysisContent = document.createElement('div')
      analysisContent.className = 'analysis-result'
      
      const resultTitle = document.createElement('h3')
      resultTitle.textContent = '分析结果'
      resultTitle.style.marginTop = '20px'
      analysisContent.appendChild(resultTitle)
      
      const resultContent = document.createElement('div')
      resultContent.className = 'result-content'
      
      analysisResult.value.sections.forEach(section => {
        const sectionDiv = document.createElement('div')
        sectionDiv.className = 'result-section'
        sectionDiv.style.marginBottom = '25px'
        sectionDiv.style.padding = '20px'
        sectionDiv.style.backgroundColor = '#f8f9fa'
        sectionDiv.style.borderRadius = '8px'
        sectionDiv.style.borderLeft = '4px solid #667eea'
        
        const sectionTitle = document.createElement('h4')
        sectionTitle.textContent = section.title
        sectionTitle.style.marginBottom = '15px'
        sectionDiv.appendChild(sectionTitle)
        
        const sectionText = document.createElement('p')
        sectionText.textContent = section.content
        sectionText.style.lineHeight = '1.6'
        sectionText.style.marginBottom = '15px'
        sectionDiv.appendChild(sectionText)
        
        const tipsList = document.createElement('div')
        tipsList.className = 'tips-list'
        
        section.tips.forEach(tip => {
          const tipItem = document.createElement('div')
          tipItem.className = 'tip-item'
          tipItem.style.display = 'flex'
          tipItem.style.alignItems = 'flex-start'
          tipItem.style.gap = '10px'
          tipItem.style.marginBottom = '10px'
          
          const tipIcon = document.createElement('span')
          tipIcon.className = 'tip-icon'
          tipIcon.textContent = '💡'
          tipItem.appendChild(tipIcon)
          
          const tipText = document.createElement('span')
          tipText.className = 'tip-text'
          tipText.textContent = tip
          tipItem.appendChild(tipText)
          
          tipsList.appendChild(tipItem)
        })
        
        sectionDiv.appendChild(tipsList)
        resultContent.appendChild(sectionDiv)
      })
      
      analysisContent.appendChild(resultContent)
      analysisCard.appendChild(analysisContent)
      analysisSection.appendChild(analysisCard)
      tempExportContainer.appendChild(analysisSection)
    }
    
    // 添加反问环节结果（如果有）
    if (generatedQuestions.value.length > 0) {
      const questionsSection = document.createElement('div')
      questionsSection.className = 'strategy-section'
      
      const questionsCard = document.createElement('div')
      questionsCard.className = 'strategy-card'
      
      const questionsTitle = document.createElement('h2')
      questionsTitle.textContent = '反问环节'
      questionsTitle.style.textAlign = 'center'
      questionsTitle.style.paddingBottom = '20px'
      questionsTitle.style.borderBottom = '2px solid #f0f0f0'
      questionsCard.appendChild(questionsTitle)
      
      const questionsContent = document.createElement('div')
      questionsContent.className = 'questions-result'
      
      const questionsListTitle = document.createElement('h3')
      questionsListTitle.textContent = '生成的问题'
      questionsListTitle.style.marginTop = '20px'
      questionsContent.appendChild(questionsListTitle)
      
      const questionsList = document.createElement('div')
      questionsList.className = 'questions-list'
      
      generatedQuestions.value.forEach((question, index) => {
        const questionCard = document.createElement('div')
        questionCard.className = 'question-card'
        questionCard.style.marginBottom = '20px'
        questionCard.style.padding = '20px'
        questionCard.style.backgroundColor = '#f8f9fa'
        questionCard.style.borderRadius = '8px'
        questionCard.style.borderLeft = '4px solid #42b883'
        
        const questionNumber = document.createElement('div')
        questionNumber.className = 'question-number'
        questionNumber.textContent = index + 1
        questionNumber.style.fontWeight = 'bold'
        questionNumber.style.color = '#42b883'
        questionNumber.style.fontSize = '1.2rem'
        questionNumber.style.marginBottom = '10px'
        questionCard.appendChild(questionNumber)
        
        const questionContent = document.createElement('div')
        questionContent.className = 'question-content'
        questionContent.textContent = question.content
        questionContent.style.lineHeight = '1.6'
        questionContent.style.marginBottom = '15px'
        questionCard.appendChild(questionContent)
        
        const questionType = document.createElement('div')
        questionType.className = 'question-type-tag'
        questionType.textContent = question.type
        questionType.style.display = 'inline-block'
        questionType.style.padding = '5px 15px'
        questionType.style.backgroundColor = '#42b883'
        questionType.style.color = 'white'
        questionType.style.borderRadius = '20px'
        questionType.style.fontSize = '0.9rem'
        questionType.style.marginBottom = '15px'
        questionCard.appendChild(questionType)
        
        const questionExplanation = document.createElement('div')
        questionExplanation.className = 'question-explanation'
        questionExplanation.style.backgroundColor = '#ffffff'
        questionExplanation.style.padding = '15px'
        questionExplanation.style.borderRadius = '5px'
        
        const explanationTitle = document.createElement('h5')
        explanationTitle.textContent = '提问意图'
        explanationTitle.style.marginBottom = '10px'
        questionExplanation.appendChild(explanationTitle)
        
        const explanationText = document.createElement('p')
        explanationText.textContent = question.explanation
        explanationText.style.fontSize = '0.95rem'
        explanationText.style.lineHeight = '1.5'
        questionExplanation.appendChild(explanationText)
        
        questionCard.appendChild(questionExplanation)
        questionsList.appendChild(questionCard)
      })
      
      questionsContent.appendChild(questionsList)
      questionsCard.appendChild(questionsContent)
      questionsSection.appendChild(questionsCard)
      tempExportContainer.appendChild(questionsSection)
    }
    
    // 将临时容器添加到文档中
    document.body.appendChild(tempExportContainer)
    
    // 使用html2canvas将临时容器转换为canvas
    const canvas = await html2canvas(tempExportContainer, {
      scale: 2, // 提高分辨率
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false
    })
    
    // 从文档中移除临时容器
    document.body.removeChild(tempExportContainer)
    
    // 创建PDF文档
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })
    
    // 定义页面配置
    const pageWidth = 210 // A4宽度，单位mm
    const pageHeight = 297 // A4高度，单位mm
    const margin = 15 // 页边距，单位mm
    const contentWidth = pageWidth - 2 * margin // 内容宽度
    
    // 将canvas转换为图片数据
    const imgData = canvas.toDataURL('image/png')
    
    // 获取canvas的尺寸（像素）
    const canvasWidth = canvas.width
    const canvasHeight = canvas.height
    
    // 计算PDF中每毫米对应的像素数
    const pixelsPerMm = canvasWidth / contentWidth
    
    // 计算单页可显示的像素高度
    const pageHeightPixels = (pageHeight - 2 * margin) * pixelsPerMm
    
    // 计算需要的页数
    const totalPages = Math.ceil(canvasHeight / pageHeightPixels)
    
    // 逐页添加内容，每次显示图像的不同部分
    for (let page = 0; page < totalPages; page++) {
      if (page > 0) {
        pdf.addPage()
      }
      
      // 计算当前页在图像中的垂直偏移量（像素）
      const yOffsetPixels = page * pageHeightPixels
      
      // 计算在PDF中的偏移量（毫米）
      const yOffsetMm = (yOffsetPixels * contentWidth) / canvasWidth
      
      // 计算当前页要显示的图像部分
      const sourceY = yOffsetPixels
      const sourceHeight = Math.min(pageHeightPixels, canvasHeight - sourceY)
      
      // 创建一个临时canvas，只包含当前页的内容
      const tempCanvas = document.createElement('canvas')
      const tempCtx = tempCanvas.getContext('2d')
      tempCanvas.width = canvasWidth
      tempCanvas.height = sourceHeight
      
      // 将当前页的图像部分绘制到临时canvas
      tempCtx.drawImage(
        canvas, 
        0, sourceY, // 源图像的起始位置
        canvasWidth, sourceHeight, // 源图像的宽度和高度
        0, 0, // 目标位置
        tempCanvas.width, tempCanvas.height // 目标尺寸
      )
      
      // 将临时canvas转换为图片数据
      const tempImgData = tempCanvas.toDataURL('image/png')
      
      // 将临时canvas绘制到PDF
      pdf.addImage(
        tempImgData,
        'PNG',
        margin, // X坐标
        margin, // Y坐标
        contentWidth, // 宽度
        (sourceHeight * contentWidth) / canvasWidth // 高度（保持比例）
      )
    }
    
    // 保存PDF文件
    pdf.save('面试策略锦囊.pdf')
  } catch (error) {
    console.error('导出PDF失败:', error)
    showErrorMessage(t('alerts.exportPdfFailed'), t('alerts.title'))
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.strategy-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.strategy-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.export-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 25px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-btn:hover {
  background-color: #5a6fd8;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.export-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.export-content {
  position: absolute;
  left: -9999px;
  top: -9999px;
  width: 100%;
  /* 导出内容只用于PDF生成，定位到页面外但保持可见 */
}

.form-content {
  margin-top: 30px;
}

.strategy-container h1 {
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.strategy-section {
  margin-bottom: 30px;
}

.strategy-card {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.strategy-card h2 {
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.strategy-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.option-group label {
  font-weight: bold;
  color: #333;
  font-size: 1.1rem;
}

.option-group textarea {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: vertical;
  font-size: 1rem;
  font-family: inherit;
  min-height: 120px;
}

.option-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.direction-options, .question-types {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.direction-checkbox, .type-checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.direction-checkbox input[type="checkbox"], .type-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #667eea;
}

.checkbox-label {
  font-size: 1rem;
  color: #333;
}

.company-inputs {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.company-input {
  flex: 1;
  min-width: 200px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.company-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.analyze-btn, .generate-questions-btn {
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

.analyze-btn:hover, .generate-questions-btn:hover {
  background-color: #369f70;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(66, 184, 131, 0.3);
}

.btn-icon {
  font-size: 1.3rem;
}

.analysis-result, .questions-result {
  background-color: #f8f9fa;
  padding: 25px;
  border-radius: 8px;
}

.analysis-result h3, .questions-result h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.4rem;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.result-section {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  border-left: 4px solid #667eea;
}

.result-section h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.2rem;
}

.result-section p {
  margin: 0 0 15px 0;
  color: #666;
  line-height: 1.6;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tip-item {
  display: flex;
  gap: 10px;
  padding: 10px;
  background-color: #f0f4ff;
  border-radius: 5px;
  align-items: flex-start;
}

.tip-icon {
  font-size: 1.1rem;
  color: #667eea;
  flex-shrink: 0;
  margin-top: 2px;
}

.tip-text {
  font-size: 0.95rem;
  line-height: 1.5;
  color: #333;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #42b883;
}

.question-number {
  font-weight: bold;
  color: #42b883;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.question-content {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
  margin-bottom: 15px;
}

.question-type-tag {
  display: inline-block;
  padding: 5px 15px;
  background-color: #42b883;
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 15px;
}

.question-explanation {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
}

.question-explanation h5 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1rem;
}

.question-explanation p {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .strategy-container {
    padding: 10px;
  }
  
  .strategy-container h1 {
    font-size: 2rem;
  }
  
  .strategy-card {
    padding: 20px;
  }
  
  .company-inputs {
    flex-direction: column;
  }
  
  .company-input {
    min-width: auto;
  }
}

/* 遮盖层样式 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  color: white;
  text-align: center;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #42b883;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-content h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
  color: #fff;
}
</style>