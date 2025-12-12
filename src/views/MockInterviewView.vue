<template>
  <div class="mock-interview-container">
    <h1>全真模拟真人面试</h1>
    
    <!-- API调用遮盖层 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <h3>{{ loadingMessage }}</h3>
        <p>请稍候，系统正在处理您的请求</p>
      </div>
    </div>
    
    <div v-if="!isInterviewStarted" class="interview-setup-section">
      <div class="setup-card">
        <h2>面试设置</h2>
        
        <div class="setup-options">
          <div class="option-group">
            <label>面试官风格</label>
            <div class="interviewer-styles">
              <div 
                v-for="style in interviewerStyles" 
                :key="style.name" 
                class="style-card" 
                :class="{ active: selectedStyle === style.name }"
                @click="selectedStyle = style.name"
              >
                <div class="style-icon">{{ style.icon }}</div>
                <h3>{{ style.name }}</h3>
                <p>{{ style.description }}</p>
              </div>
            </div>
          </div>



          <div class="option-group">
            <label>面试时长</label>
            <div class="duration-options">
              <button 
                v-for="duration in durations" 
                :key="duration" 
                :class="['duration-btn', { active: selectedDuration === duration }]" 
                @click="selectedDuration = duration"
              >
                {{ duration }}分钟
              </button>
            </div>
          </div>

          <button class="start-btn" @click="startInterview">
            <span class="btn-icon">🚀</span>
            开始模拟面试
          </button>
        </div>
      </div>
    </div>

    <div v-else class="interview-main-section">
      <div class="interview-header">
        <div class="interview-info">
          <span class="style-badge">{{ selectedStyle }}</span>
          <span class="duration-badge">{{ selectedDuration }}分钟</span>
        </div>
        <div class="interview-actions">
          <button class="action-btn" @click="pauseInterview">
            <span class="action-icon">{{ isPaused ? '▶️' : '⏸️' }}</span>
            {{ isPaused ? '继续' : '暂停' }}
          </button>
          <button class="action-btn danger" @click="endInterview">
            <span class="action-icon">⏹️</span>
            结束面试
          </button>
        </div>
      </div>

      <div class="interview-content">
        <div class="chat-container">
          <div class="chat-messages" ref="chatMessages">
            <div 
              v-for="(message, index) in messages" 
              :key="index" 
              class="message" 
              :class="{ 'user-message': message.sender === 'user', 'ai-message': message.sender === 'ai' }"
            >
              <div class="message-avatar">
                {{ message.sender === 'user' ? '👤' : '🤖' }}
              </div>
              <div class="message-content">
                <div class="message-sender">{{ message.sender === 'user' ? '我' : '面试官' }}</div>
                <div class="message-text">{{ message.text }}</div>
                <div class="message-time">{{ message.time }}</div>
              </div>
            </div>
          </div>

          <div class="chat-input-area">
            <div class="text-input-container">
              <div class="voice-status-indicator" :class="recordingStatus">
                <span class="status-icon">{{ 
                  recordingStatus === 'recording' ? '🔴' : 
                  recordingStatus === 'processing' ? '⏳' : 
                  recordingStatus === 'completed' ? '✅' : 
                  recordingStatus === 'starting' ? '📤' : '🎤' 
                }}</span>
                <span class="status-text">{{ 
                  recordingStatus === 'recording' ? '录音中...' : 
                  recordingStatus === 'processing' ? '处理中...' : 
                  recordingStatus === 'completed' ? '已完成' : 
                  recordingStatus === 'starting' ? '准备中...' : '点击开始录音' 
                }}</span>
              </div>
              <textarea 
                v-model="inputMessage" 
                placeholder="请输入您的回答..."
                rows="3"
                @keydown.enter.prevent="sendMessage"
              ></textarea>
              <div class="input-actions">
                <button class="voice-btn" :class="recordingStatus" @click="toggleRecording">
                  <span class="voice-icon">{{ isRecording ? '🔴' : '🎤' }}</span>
                  {{ isRecording ? '停止录音' : '开始录音' }}
                </button>
                <button class="send-btn" @click="sendMessage">
                  <span class="send-icon">📤</span>
                  发送
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="interview-sidebar">
          <div class="sidebar-section">
            <h3>面试进度</h3>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progress + '%' }"></div>
            </div>
            <div class="progress-info">
              <span>{{ currentQuestion }} / {{ totalQuestions }}</span>
              <span>剩余时间: {{ Math.max(0, remainingTime).toFixed(1) }}分钟</span>
            </div>
          </div>

          <div class="sidebar-section">
            <h3>问题列表</h3>
            <div class="question-list">
              <div 
                v-for="(q, index) in askedQuestions" 
                :key="index" 
                class="question-item"
              >
                <div class="question-number">{{ index + 1 }}</div>
                <div class="question-text">{{ q }}</div>
              </div>
            </div>
          </div>

          <div class="sidebar-section">
            <h3>实时提示</h3>
            <div class="tips-list">
              <div class="tip-item" v-for="(tip, index) in realTimeTips" :key="index">
                <span class="tip-icon">💡</span>
                <span class="tip-text">{{ tip }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showReport" class="report-section">
      <div class="report-card" ref="reportCard">
        <h2>面试复盘报告</h2>
        
        <div class="report-header">
          <div class="report-info">
            <span class="report-badge">面试完成</span>
            <span class="report-date">{{ new Date().toLocaleString() }}</span>
          </div>
        </div>

        <div class="report-content">
          <div class="radar-chart-section">
            <h3>多维能力评估</h3>
            <div class="radar-chart-placeholder">
              <div class="radar-chart">
                <div class="radar-axis">
                  <div class="radar-label">专业能力</div>
                  <div class="radar-value">{{ reportData.professionalScore }}</div>
                </div>
                <div class="radar-axis">
                  <div class="radar-label">逻辑表达</div>
                  <div class="radar-value">{{ reportData.logicScore }}</div>
                </div>
                <div class="radar-axis">
                  <div class="radar-label">自信程度</div>
                  <div class="radar-value">{{ reportData.confidenceScore }}</div>
                </div>
                <div class="radar-axis">
                  <div class="radar-label">岗位匹配度</div>
                  <div class="radar-value">{{ reportData.matchScore }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="detailed-analysis-section">
            <h3>逐题诊断</h3>
            <div class="analysis-list">
              <div 
                v-for="(analysis, index) in reportData.questionAnalysis" 
                :key="index" 
                class="analysis-item"
              >
                <div class="analysis-question">
                  <strong>问题 {{ index + 1 }}:</strong> {{ analysis.question }}
                </div>
                <div class="analysis-answer">
                  <strong>您的回答:</strong> {{ analysis.answer }}
                </div>
                <div class="analysis-feedback">
                  <strong>反馈:</strong> {{ analysis.feedback }}
                </div>
                <div class="analysis-suggestion">
                  <strong>建议:</strong> {{ analysis.suggestion }}
                </div>
              </div>
            </div>
          </div>

          <div class="optimization-section">
            <h3>优化建议</h3>
            <div class="suggestions-list" ref="suggestionsList">
              <div class="suggestion-item" v-for="(suggestion, index) in reportData.optimizationSuggestions" :key="index">
                <span class="suggestion-icon">📋</span>
                <span class="suggestion-text">{{ suggestion }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="report-footer">
          <button class="action-btn" @click="saveReport">
            <span class="action-icon">💾</span>
            保存报告
          </button>
          <button class="action-btn" @click="newInterview">
            <span class="action-icon">🔄</span>
            重新开始
          </button>
          <router-link to="/" class="action-btn">
            <span class="action-icon">🏠</span>
            返回首页
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

const router = useRouter()

const isInterviewStarted = ref(false)
const isPaused = ref(false)
const isRecording = ref(false)
const showReport = ref(false)
const selectedStyle = ref('温柔HR')
const selectedDuration = ref(15)
const inputMessage = ref('')
const messages = ref([])
const askedQuestions = ref([])
const realTimeTips = ref([])
const currentQuestion = ref(1)
const totalQuestions = ref(10)
const progress = ref(0)
const remainingTime = ref(selectedDuration.value)
const chatMessages = ref(null)
const reportCard = ref(null)
const suggestionsList = ref(null)
const isLoading = ref(false)
const loadingMessage = ref('正在处理请求...')
const interviewId = ref(null)
const isEnding = ref(false)
let timer = null

const interviewerStyles = [
  { name: '温柔HR', icon: '😊', description: '友好亲切，适合初次面试练习' },
  { name: '严厉技术总监', icon: '😐', description: '专业严谨，适合技术岗位准备' },
  { name: '综合面试官', icon: '🤔', description: '平衡风格，适合综合练习' }
]

const durations = [15, 30, 45, 60]

// 监听面试设置变化，实时从后端获取匹配的历史记录
const setupWatchers = () => {
  // 当面试设置变化时，实时从后端获取匹配的历史记录
  watch([selectedStyle, selectedDuration], () => {
    fetchMockInterviewHistory()
  })
}

const reportData = ref({
  professionalScore: 85,
  logicScore: 78,
  confidenceScore: 82,
  matchScore: 80,
  questionAnalysis: [
    {
      question: '请介绍一下你自己',
      answer: '我是一名前端开发工程师，有5年工作经验...',
      feedback: '回答结构清晰，重点突出，但可以更具体地描述项目成果',
      suggestion: '建议使用STAR法则，增加数据支撑'
    }
  ],
  optimizationSuggestions: [
    '加强专业术语的使用，提升专业性',
    '注意语速控制，保持清晰流畅',
    '增加具体案例，增强说服力',
    '加强与面试官的眼神交流（视频面试）'
  ]
})

// 历史面试记录
const interviewHistory = ref([])

const startInterview = async () => {
  // 直接开始面试，不再根据模式检测设备
  await startInterviewProcess()
}

// 实际开始面试的处理函数
const startInterviewProcess = async () => {
  isLoading.value = true
  loadingMessage.value = '正在准备面试...'
  
  // 从localStorage获取userId
  const userId = localStorage.getItem('userId') || ''
  
  try {
    // 调用后端API开始面试
    const response = await axios.post('http://127.0.0.1:5000/api/mock-interview/start', {
      userId: userId,
      style: selectedStyle.value,
      duration: selectedDuration.value
    })
    
    const data = response.data
    interviewId.value = data.interviewId
    isInterviewStarted.value = true
    remainingTime.value = selectedDuration.value
    messages.value = [
      {
        sender: 'ai',
        text: `您好！我是今天的面试官，我们将进行一场${selectedDuration.value}分钟的${selectedStyle.value}风格面试。现在开始我们的面试，首先请您回答：${data.currentQuestion.content}`,
        time: getCurrentTime()
      }
    ]
    askedQuestions.value = [data.currentQuestion.content]
    realTimeTips.value = data.tips
    startTimer()
  } catch (error) {
    console.error('开始面试失败:', error)
    // 检查是否是用户不存在的错误
    if (error.response && error.response.data.error === 'User not found') {
      alert('请先上传简历进行优化，然后再开始模拟面试')
      router.push('/resume')
    } else {
      alert('开始面试失败，请重试')
    }
  } finally {
    isLoading.value = false
  }
}

const pauseInterview = () => {
  isPaused.value = !isPaused.value
  if (isPaused.value) {
    clearInterval(timer)
  } else {
    startTimer()
  }
}

const endInterview = () => {
  // 防止重复调用
  if (isEnding.value) return
  
  isEnding.value = true
  isLoading.value = true
  loadingMessage.value = '正在生成面试报告...'
  
  // 从localStorage获取userId
  const userId = localStorage.getItem('userId') || ''
  
  // 调用后端API结束面试，获取报告
  axios.post('http://127.0.0.1:5000/api/mock-interview/end', {
    interviewId: interviewId.value,
    userId: userId,
    style: selectedStyle.value,
    duration: selectedDuration.value
  })
  .then(response => {
    reportData.value = response.data
    showReport.value = true
    isInterviewStarted.value = false
    clearInterval(timer)
    
  })
  .catch(error => {
    console.error('结束面试失败:', error)
    alert('结束面试失败，请重试')
  })
  .finally(() => {
    isLoading.value = false
    isEnding.value = false
  })
}

const startTimer = () => {
  timer = setInterval(() => {
    remainingTime.value -= 0.1
    if (remainingTime.value <= 0) {
      endInterview()
    }
    progress.value = Math.min(100, (currentQuestion.value / totalQuestions.value) * 100)
  }, 10000) // 每10秒更新一次
}

const sendMessage = () => {
  if (!inputMessage.value.trim() || !interviewId.value) return
  
  isLoading.value = true
  loadingMessage.value = '正在分析您的回答...'
  const userAnswer = inputMessage.value
  
  // 添加用户消息
  messages.value.push({
    sender: 'user',
    text: userAnswer,
    time: getCurrentTime()
  })
  
  inputMessage.value = ''
  scrollToBottom()
  
  // 调用后端API回答问题
  axios.post('http://127.0.0.1:5000/api/mock-interview/answer', {
    interviewId: interviewId.value,
    questionId: currentQuestion.value,
    answer: userAnswer
  })
  .then(response => {
    const data = response.data
    
    // 添加AI消息
    messages.value.push({
      sender: 'ai',
      text: `感谢您的回答。${data.feedback} 接下来请您回答：${data.nextQuestion.content}`,
      time: getCurrentTime()
    })
    
    askedQuestions.value.push(data.nextQuestion.content)
    currentQuestion.value++
    scrollToBottom()
    
    if (currentQuestion.value > totalQuestions.value) {
      endInterview()
    }
  })
  .catch(error => {
    console.error('回答问题失败:', error)
    alert('回答问题失败，请重试')
  })
  .finally(() => {
    isLoading.value = false
  })
}

// 语音识别相关变量
let recognition = null
let isSpeechSupported = ref(true)
// 添加语音识别状态管理变量（在组件作用域内定义）
let isRecognitionStarting = false
let isRecognitionRunning = false
// 添加录音状态指示
const recordingStatus = ref('idle') // idle, recording, processing, completed
// 保存当前录音的临时文本，用于追加功能
let currentRecordingText = ''
// 保存上一次最终结果的位置，用于实现追加功能
let lastFinalIndex = 0

// 初始化语音识别
const initSpeechRecognition = () => {
  // 检查浏览器是否支持语音识别
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  const SpeechGrammarList = window.SpeechGrammarList || window.webkitSpeechGrammarList
  const SpeechRecognitionEvent = window.SpeechRecognitionEvent || window.webkitSpeechRecognitionEvent
  
  if (!SpeechRecognition) {
    isSpeechSupported.value = false
    realTimeTips.value.push('您的浏览器不支持语音识别功能，请使用Chrome或Edge等现代浏览器')
    return
  }
  
  console.log('创建语音识别实例...')
  // 创建语音识别实例
  recognition = new SpeechRecognition()
  
  // 设置语音识别选项
  recognition.continuous = true // 持续识别，避免停顿几秒后自动终止
  recognition.interimResults = true // 返回中间结果
  recognition.lang = 'zh-CN' // 设置为中文
  recognition.maxAlternatives = 1 // 只返回一个结果
  
  // 监听语音识别开始事件
  recognition.onstart = () => {
    console.log('✅ 语音识别已开始')
    isRecognitionStarting = false
    isRecognitionRunning = true
    recordingStatus.value = 'recording'
    realTimeTips.value.push('🎤 录音中...')
    // 保存当前输入框内容，用于后续追加
    currentRecordingText = inputMessage.value
    // 保存当前录音的起始索引，用于标点符号处理
    lastFinalIndex = event ? event.results.length : 0
  }
  
  // 监听语音识别结果事件
  recognition.onresult = (event) => {
    console.log('🔊 收到语音识别结果事件:', event)
    
    // 初始化当前录音的转录文本
    let newTranscript = ''
    let hasFinalResult = false
    
    // 遍历所有结果（包括中间结果）
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const result = event.results[i]
      const item = result[0]
      
      console.log(`结果 ${i}:`, {
        transcript: item.transcript,
        isFinal: result.isFinal,
        confidence: item.confidence
      })
      
      // 拼接转录文本
      newTranscript += item.transcript
      
      // 如果是最终结果
      if (result.isFinal) {
        hasFinalResult = true
        lastFinalIndex = i
        
        // 添加标点符号处理：在最终结果末尾添加适当的标点
        // 检查是否已经有标点符号
        const lastChar = newTranscript.slice(-1)
        if (!['。', '，', '！', '？', '；', '.', ',', '!', '?', ';'].includes(lastChar)) {
          // 如果是较长的文本，添加句号；否则添加逗号
          if (newTranscript.length > 10) {
            newTranscript += '。'
          } else {
            newTranscript += '，'
          }
        }
      }
    }
    
    console.log('📝 当前录音转录文本:', newTranscript)
    
    // 更新输入框内容：当前输入框内容 + 新转录的内容
    const fullText = currentRecordingText + newTranscript
    console.log('✅ 更新输入框内容:', fullText)
    inputMessage.value = fullText
    
    // 如果有最终结果，更新当前录音文本，以便下次追加
    if (hasFinalResult) {
      currentRecordingText = fullText
    }
  }
  
  // 监听语音识别错误事件
  recognition.onerror = (event) => {
    console.error('❌ 语音识别错误:', event.error)
    recordingStatus.value = 'idle'
    
    // 只处理真正的致命错误，忽略网络错误等非致命错误
    const fatalErrors = ['not-allowed', 'audio-capture']
    
    if (fatalErrors.includes(event.error)) {
      let errorMessage = '语音识别失败，请重试'
      
      if (event.error === 'not-allowed') {
        errorMessage = '麦克风权限被拒绝，请在浏览器设置中允许麦克风访问'
      } else if (event.error === 'audio-capture') {
        errorMessage = '未检测到麦克风设备'
      }
      
      realTimeTips.value.push(errorMessage)
      isRecording.value = false
    } 
    else {
      console.log(`⚠️  非致命错误: ${event.error}，继续录音...`)
      
      // 对于网络错误，显示友好提示，但不停止录音
      if (event.error === 'network') {
        realTimeTips.value.push('网络连接暂时不稳定，语音识别正在尝试恢复...')
      }
    }
  }
  
  // 监听语音识别结束事件
  recognition.onend = () => {
    console.log('⏹️  语音识别已结束')
    isRecognitionRunning = false
    recordingStatus.value = 'completed'
    realTimeTips.value.push('✅ 录音已完成')
    
    // 重置状态
    setTimeout(() => {
      recordingStatus.value = 'idle'
    }, 1000)
  }
}

// 在组件挂载时初始化语音识别
onMounted(() => {
  realTimeTips.value = [
    '保持微笑，展现自信',
    '回答问题时保持逻辑清晰',
    '注意控制语速，避免过快或过慢'
  ]
  
  // 设置监听器
  setupWatchers()
  
  // 获取用户的模拟面试历史记录
  fetchMockInterviewHistory()
  
  // 初始化语音识别
  initSpeechRecognition()
})

// 组件卸载时停止语音识别
onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
  if (recognition && recognition.state === 'running') {
    recognition.stop()
  }
})

const toggleRecording = async () => {
  if (!isSpeechSupported.value) {
    alert('您的浏览器不支持语音识别功能，请使用Chrome或Edge等现代浏览器')
    return
  }
  
  if (isRecording.value) {
    // 停止录音
    console.log('停止录音...')
    recordingStatus.value = 'processing'
    realTimeTips.value.push('⏳ 正在处理录音...')
    
    // 停止语音识别
    if (recognition && (recognition.state === 'running' || recognition.state === 'starting')) {
      recognition.stop()
    }
    
    isRecording.value = false
    
    // 延迟更新状态，让用户看到处理过程
    setTimeout(() => {
      recordingStatus.value = 'completed'
      realTimeTips.value.push('✅ 录音已完成')
      
      // 1秒后恢复空闲状态
      setTimeout(() => {
        recordingStatus.value = 'idle'
      }, 1000)
    }, 500)
  } else {
    // 开始录音
    isRecording.value = true
    recordingStatus.value = 'starting'
    realTimeTips.value.push('📤 正在准备录音...')
    
    try {
      // 检查浏览器是否支持权限查询API
      if (navigator.permissions && navigator.permissions.query) {
        // 查询麦克风权限状态
        const permissionStatus = await navigator.permissions.query({ name: 'microphone' })
        
        if (permissionStatus.state === 'denied') {
          // 权限已被拒绝，提醒用户去设置
          realTimeTips.value.push('❌ 麦克风权限被拒绝，请在浏览器设置中允许麦克风访问')
          isRecording.value = false
          recordingStatus.value = 'idle'
          // 可以添加一个更明显的提示
          alert('麦克风权限被拒绝，请在浏览器设置中允许麦克风访问后重试')
          return
        } 
        // 如果是prompt状态，会在getUserMedia时弹出权限请求
      }
      
      // 请求麦克风权限
      await navigator.mediaDevices.getUserMedia({ audio: true })
      
      // 开始语音识别
      console.log('开始语音识别...')
      recognition.start()
    } catch (error) {
      console.error('开始录音失败:', error)
      let errorMessage = '无法访问麦克风设备，请检查权限设置'
      
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        errorMessage = '麦克风权限被拒绝，请在浏览器设置中允许麦克风访问'
        // 添加更明显的提示
        alert('麦克风权限被拒绝，请在浏览器设置中允许麦克风访问后重试')
      } else if (error.name === 'NotFoundError' || error.message.includes('No device found')) {
        errorMessage = '未检测到麦克风设备，请连接麦克风后重试'
      } else if (error.name === 'NotReadableError') {
        errorMessage = '麦克风设备被占用，请关闭其他使用麦克风的应用'
      } else if (error.name === 'OverconstrainedError') {
        errorMessage = '无法满足录音设备要求，请尝试调整麦克风设置'
      }
      
      realTimeTips.value.push(`❌ ${errorMessage}`)
      isRecording.value = false
      recordingStatus.value = 'idle'
    }
  }
}

const saveReport = async () => {
  if (!reportCard.value) return
  
  try {
    isLoading.value = true
    loadingMessage.value = '正在生成PDF报告...'
    
    // 临时调整样式，确保所有内容都能被捕获
    const originalStyles = []
    // 只需要处理question-list和analysis-list，suggestions-list已经默认展开
    const scrollableElements = document.querySelectorAll('.question-list, .analysis-list')
    
    // 移除滚动限制，让所有内容展开
    scrollableElements.forEach(el => {
      originalStyles.push({
        element: el,
        maxHeight: el.style.maxHeight,
        overflowY: el.style.overflowY
      })
      el.style.maxHeight = 'none'
      el.style.overflowY = 'visible'
    })
    
    // 等待DOM更新
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // 使用html2canvas将HTML转换为canvas
    const canvas = await html2canvas(reportCard.value, {
      scale: 2, // 提高清晰度
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false
    })
    
    // 恢复原始样式
    originalStyles.forEach(({ element, maxHeight, overflowY }) => {
      element.style.maxHeight = maxHeight
      element.style.overflowY = overflowY
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
    doc.save('面试复盘报告.pdf')
  } catch (error) {
    console.error('生成PDF失败:', error)
    alert('生成PDF失败，请重试')
  } finally {
    isLoading.value = false
  }
}

const newInterview = () => {
  showReport.value = false
  isInterviewStarted.value = false
  messages.value = []
  askedQuestions.value = []
  realTimeTips.value = []
  currentQuestion.value = 1
  progress.value = 0
  remainingTime.value = selectedDuration.value
  interviewId.value = null
  isEnding.value = false
}

const getCurrentTime = () => {
  const now = new Date()
  return now.toLocaleTimeString()
}

const scrollToBottom = () => {
  setTimeout(() => {
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight
    }
  }, 100)
}

// 获取用户的模拟面试历史记录
const fetchMockInterviewHistory = async () => {
  try {
    const userId = localStorage.getItem('userId')
    if (!userId) return
    
    // 发送当前选择的style和duration参数
    const response = await axios.get(`http://127.0.0.1:5000/api/mock-interview/history`, {
      params: {
        userId: userId,
        style: selectedStyle.value,
        duration: selectedDuration.value
      }
    })
    // 保存历史记录
    interviewHistory.value = response.data || []
    console.log('模拟面试历史记录:', interviewHistory.value)
    
    // 检查是否有匹配的历史记录，如果有则自动加载
    checkAndLoadMatchingReport()
  } catch (error) {
    console.error('获取模拟面试历史记录失败:', error)
    // 检查是否是用户不存在的错误
    if (error.response && error.response.data.error === 'User not found') {
      alert('请先上传简历进行优化，然后再开始模拟面试')
      router.push('/resume')
    }
  }
}

// 检查并加载匹配的历史记录
const checkAndLoadMatchingReport = () => {
  console.log('开始检查匹配的历史记录...')
  console.log('当前历史记录数量:', interviewHistory.value.length)
  console.log('当前选择的设置:', {
    style: selectedStyle.value,
    duration: selectedDuration.value
  })
  
  if (interviewHistory.value.length === 0) {
    console.log('没有历史记录，隐藏报告')
    showReport.value = false
    return
  }
  
  // 后端已经根据筛选条件返回了最新的一条记录，直接使用即可
  const matchingHistory = interviewHistory.value[0]
  console.log('后端返回的历史记录:', matchingHistory)
  
  // 检查返回的记录是否与当前选择的设置匹配
  if (matchingHistory.style === selectedStyle.value && 
      Math.abs(matchingHistory.duration - selectedDuration.value) <= 5) {
    
    if (matchingHistory.reportData) {
      console.log('历史记录包含reportData，开始加载报告')
      reportData.value = matchingHistory.reportData
      showReport.value = true
      console.log('报告已加载，showReport:', showReport.value)
    } else {
      console.log('历史记录不包含reportData，跳过加载')
      showReport.value = false
    }
  } else {
    console.log('后端返回的记录与当前选择的设置不匹配，隐藏报告')
    showReport.value = false
  }
}

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.mock-interview-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.mock-interview-container h1 {
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.setup-card, .report-card {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.setup-card h2, .report-card h2 {
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.setup-options {
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

.interviewer-styles {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.style-card {
  padding: 25px;
  background-color: #f8f9fa;
  border: 2px solid #ddd;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  min-width: 200px;
  flex: 1;
  max-width: 300px;
}

.style-card:hover {
  border-color: #667eea;
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.style-card.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.style-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.style-card h3 {
  margin: 0 0 10px 0;
  font-size: 1.3rem;
}

.style-card p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

.interaction-modes, .duration-options {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.mode-btn, .duration-btn {
  padding: 15px 30px;
  border: 2px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.mode-btn:hover, .duration-btn:hover {
  border-color: #667eea;
}

.mode-btn.active, .duration-btn.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.mode-icon {
  font-size: 1.2rem;
}

.start-btn {
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

.start-btn:hover {
  background-color: #369f70;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(66, 184, 131, 0.3);
}

.btn-icon {
  font-size: 1.3rem;
}

.interview-main-section {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.interview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
  flex-wrap: wrap;
  gap: 20px;
}

.interview-info {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.style-badge, .mode-badge, .duration-badge, .report-badge {
  padding: 8px 15px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.style-badge {
  background-color: #667eea;
  color: white;
}

.mode-badge {
  background-color: #42b883;
  color: white;
}

.duration-badge {
  background-color: #f093fb;
  color: white;
}

.report-badge {
  background-color: #4facfe;
  color: white;
}

.interview-actions, .report-footer {
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
  text-decoration: none;
}

.action-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.action-btn.danger {
  border-color: #ff4757;
  color: #ff4757;
}

.action-btn.danger:hover {
  background-color: #ff4757;
  color: white;
}

.action-icon {
  font-size: 1.1rem;
}

.interview-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chat-messages {
  flex: 1;
  height: 500px;
  overflow-y: auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  display: flex;
  gap: 15px;
  max-width: 80%;
}

.message.user-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.ai-message {
  align-self: flex-start;
}

.message-avatar {
  font-size: 2rem;
  flex-shrink: 0;
}

.message-content {
  background-color: white;
  padding: 15px;
  border-radius: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.user-message .message-content {
  background-color: #667eea;
  color: white;
}

.message-sender {
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.user-message .message-sender {
  text-align: right;
}

.message-text {
  line-height: 1.6;
  margin-bottom: 5px;
  word-wrap: break-word;
}

.message-time {
  font-size: 0.8rem;
  opacity: 0.7;
}

.user-message .message-time {
  text-align: right;
}

.chat-input-area {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.text-input-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: stretch;
}

.voice-status-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 15px;
  border-radius: 5px;
  font-weight: bold;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.voice-status-indicator.idle {
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #ddd;
}

.voice-status-indicator.starting {
  background-color: #e3f2fd;
  color: #1976d2;
  border: 1px solid #90caf9;
}

.voice-status-indicator.recording {
  background-color: #ffebee;
  color: #d32f2f;
  border: 1px solid #ef5350;
  animation: pulse 1s infinite;
}

.voice-status-indicator.processing {
  background-color: #fff3e0;
  color: #f57c00;
  border: 1px solid #ffb74d;
}

.voice-status-indicator.completed {
  background-color: #e8f5e8;
  color: #388e3c;
  border: 1px solid #81c784;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.status-icon {
  font-size: 1.2rem;
}

.status-text {
  flex: 1;
}

.voice-btn.recording {
  background-color: #d32f2f;
  animation: pulse 1s infinite;
}

.input-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.text-input-container textarea {
  flex: 1;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: vertical;
  font-size: 1rem;
  font-family: inherit;
}

.text-input-container textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.send-btn {
  padding: 15px 30px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.send-btn:hover {
  background-color: #5568d3;
  transform: translateY(-2px);
}

.send-icon {
  font-size: 1.1rem;
}

.voice-input-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
}

.device-selector {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  width: 100%;
  max-width: 400px;
}

.device-selector label {
  font-weight: bold;
  color: #333;
  font-size: 1rem;
}

.device-selector select {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.device-selector select:hover {
  border-color: #667eea;
}

.device-selector select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.voice-status {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  font-weight: bold;
  color: #667eea;
}

.voice-icon {
  font-size: 1.5rem;
}

.voice-btn {
  padding: 20px 40px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  min-width: 200px;
}

.voice-btn:hover {
  background-color: #5568d3;
  transform: scale(1.05);
}

.voice-btn:active {
  transform: scale(0.95);
}

.interview-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-section {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.sidebar-section h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.1rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
}

.progress-bar {
  height: 10px;
  background-color: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress-fill {
  height: 100%;
  background-color: #667eea;
  transition: width 0.3s ease;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
}

.question-list, .tips-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 200px;
  overflow-y: auto;
}

/* 优化建议内容直接全部展示，不需要滚动框 */
.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: none;
  overflow-y: visible;
}

.question-item {
  display: flex;
  gap: 10px;
  padding: 10px;
  background-color: white;
  border-radius: 5px;
  border-left: 3px solid #667eea;
}

.question-number {
  font-weight: bold;
  color: #667eea;
  flex-shrink: 0;
  min-width: 20px;
}

.question-text {
  font-size: 0.9rem;
  line-height: 1.4;
  color: #333;
}

.tip-item, .suggestion-item {
  display: flex;
  gap: 10px;
  padding: 10px;
  background-color: white;
  border-radius: 5px;
  align-items: flex-start;
}

.tip-icon, .suggestion-icon {
  font-size: 1.1rem;
  color: #667eea;
  flex-shrink: 0;
  margin-top: 2px;
}

.tip-text, .suggestion-text {
  font-size: 0.9rem;
  line-height: 1.4;
  color: #333;
}

.report-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.report-info {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.report-date {
  color: #666;
  font-size: 0.9rem;
}

.report-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.radar-chart-section, .detailed-analysis-section, .optimization-section {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.radar-chart-section h3, .detailed-analysis-section h3, .optimization-section h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.2rem;
}

.radar-chart-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}

.radar-chart {
  display: flex;
  gap: 30px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.radar-axis {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.radar-label {
  font-weight: bold;
  color: #333;
  text-align: center;
}

.radar-value {
  width: 80px;
  height: 80px;
  background-color: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.analysis-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.analysis-item {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.analysis-item strong {
  color: #333;
}

.analysis-item div {
  margin-bottom: 10px;
  line-height: 1.6;
}

.analysis-item div:last-child {
  margin-bottom: 0;
}

.report-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #f0f0f0;
  justify-content: center;
}

@media (max-width: 768px) {
  .mock-interview-container {
    padding: 10px;
  }
  
  .mock-interview-container h1 {
    font-size: 2rem;
  }
  
  .setup-card, .report-card {
    padding: 20px;
  }
  
  .interviewer-styles {
    grid-template-columns: 1fr;
  }
  
  .interview-content {
    grid-template-columns: 1fr;
  }
  
  .chat-messages {
    height: 400px;
  }
  
  .text-input-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .message {
    max-width: 95%;
  }
  
  .radar-chart {
    flex-direction: column;
  }
}

/* API调用遮盖层样式 */
.loading-overlay {
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

.loading-content {
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

.loading-content h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.loading-content p {
  color: #666;
  margin: 0;
  font-size: 1rem;
}
</style>