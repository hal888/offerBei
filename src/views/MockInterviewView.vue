<template>
  <div class="mock-interview-container">
    <h1>{{ $t('pages.mockInterview.title') }}</h1>
    
    <!-- API调用遮盖层 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <h3>{{ loadingMessage }}</h3>
        <p>{{ t('loading.processing') }}</p>
      </div>
    </div>
    
    <div v-if="!isInterviewStarted" class="interview-setup-section">
      <div class="setup-card">
        <h2>{{ $t('pages.mockInterview.setup.title') }}</h2>
        
        <div class="setup-options">
          <div class="option-group">
            <label>{{ $t('pages.mockInterview.setup.styleLabel') }}</label>
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
            <label>{{ $t('pages.mockInterview.setup.durationLabel') }}</label>
            <div class="duration-options">
              <button 
                v-for="duration in durations" 
                :key="duration" 
                :class="['duration-btn', { active: selectedDuration === duration }]" 
                @click="selectedDuration = duration"
              >
                {{ duration }}{{ $t('pages.mockInterview.setup.minutes') }}
              </button>
            </div>
          </div>

          <button class="start-btn" @click="startInterview">
            <span class="btn-icon">🚀</span>
            {{ $t('pages.mockInterview.start') }}
          </button>
        </div>
      </div>
    </div>

    <div v-else class="interview-main-section">
      <div class="interview-header">
        <div class="interview-info">
          <span class="style-badge">{{ selectedStyle }}</span>
          <span class="duration-badge">{{ selectedDuration }}{{ $t('pages.mockInterview.setup.minutes') }}</span>
        </div>
        <div class="interview-actions">
          <button class="action-btn" @click="pauseInterview">
            <span class="action-icon">{{ isPaused ? '▶️' : '⏸️' }}</span>
            {{ isPaused ? $t('pages.mockInterview.resume') : $t('pages.mockInterview.pause') }}
          </button>
          <button class="action-btn danger" @click="endInterview">
            <span class="action-icon">⏹️</span>
            {{ $t('pages.mockInterview.end') }}
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
                <div class="message-sender">{{ message.sender === 'user' ? $t('pages.mockInterview.chat.me') : $t('pages.mockInterview.chat.interviewer') }}</div>
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
                  recordingStatus === 'recording' ? $t('pages.mockInterview.voice.recording') :
                  recordingStatus === 'processing' ? $t('pages.mockInterview.voice.processing') :
                  recordingStatus === 'completed' ? $t('pages.mockInterview.voice.completed') :
                  recordingStatus === 'starting' ? $t('pages.mockInterview.voice.preparing') : $t('pages.mockInterview.voice.clickToStart') 
                }}</span>
              </div>
              <textarea 
                v-model="inputMessage" 
                :placeholder="$t('pages.mockInterview.answer.placeholder')"
                rows="3"
                @keydown.enter.prevent="sendMessage"
              ></textarea>
              <div class="input-actions">
                <button class="voice-btn" :class="recordingStatus" @click="toggleRecording">
                  <span class="voice-icon">{{ isRecording ? '🔴' : '🎤' }}</span>
                  {{ isRecording ? $t('pages.mockInterview.voice.stopRecording') : $t('pages.mockInterview.voice.startRecording') }}
                </button>
                <button class="send-btn" @click="sendMessage">
                  <span class="send-icon">📤</span>
                  {{ $t('pages.mockInterview.chat.send') }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="interview-sidebar">
          <div class="sidebar-section">
            <h3>{{ $t('pages.mockInterview.progress.title') }}</h3>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progress + '%' }"></div>
            </div>
            <div class="progress-info">
              <span>{{ currentQuestion }} / {{ totalQuestions }}</span>
              <span>{{ $t('pages.mockInterview.progress.timeRemaining') }}: {{ Math.max(0, remainingTime).toFixed(1) }}{{ $t('pages.mockInterview.setup.minutes') }}</span>
            </div>
          </div>

          <div class="sidebar-section">
            <h3>{{ $t('pages.mockInterview.progress.questions') }}</h3>
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
            <h3>{{ $t('pages.mockInterview.progress.tips') }}</h3>
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
        <h2>{{ $t('pages.mockInterview.report.title') }}</h2>
        
        <div class="report-header">
          <div class="report-info">
            <span class="report-badge">{{ $t('pages.mockInterview.report.completed') }}</span>
            <span class="report-date">{{ new Date().toLocaleString() }}</span>
          </div>
        </div>

        <div class="report-content">
          <div class="radar-chart-section">
            <h3>{{ $t('pages.mockInterview.report.assessment') }}</h3>
            <div class="radar-chart-placeholder">
              <div class="radar-chart">
                <div class="radar-axis">
                  <div class="radar-label">{{ $t('pages.mockInterview.report.dimensions.professional') }}</div>
                  <div class="radar-value">{{ reportData.professionalScore }}</div>
                </div>
                <div class="radar-axis">
                  <div class="radar-label">{{ $t('pages.mockInterview.report.dimensions.logic') }}</div>
                  <div class="radar-value">{{ reportData.logicScore }}</div>
                </div>
                <div class="radar-axis">
                  <div class="radar-label">{{ $t('pages.mockInterview.report.dimensions.confidence') }}</div>
                  <div class="radar-value">{{ reportData.confidenceScore }}</div>
                </div>
                <div class="radar-axis">
                  <div class="radar-label">{{ $t('pages.mockInterview.report.dimensions.match') }}</div>
                  <div class="radar-value">{{ reportData.matchScore }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="detailed-analysis-section">
            <h3>{{ $t('pages.mockInterview.report.analysis') }}</h3>
            <div class="analysis-list">
              <div 
                v-for="(analysis, index) in reportData.questionAnalysis" 
                :key="index" 
                class="analysis-item"
              >
                <div class="analysis-question">
                  <strong>{{ $t('pages.mockInterview.report.questionLabel') }} {{ index + 1 }}:</strong> {{ analysis.question }}
                </div>
                <div class="analysis-answer">
                  <strong>{{ $t('pages.mockInterview.report.yourAnswer') }}:</strong> {{ analysis.answer }}
                </div>
                <div class="analysis-feedback">
                  <strong>{{ $t('pages.mockInterview.report.feedbackLabel') }}:</strong> {{ analysis.feedback }}
                </div>
                <div class="analysis-suggestion">
                  <strong>{{ $t('pages.mockInterview.report.suggestionLabel') }}:</strong> {{ analysis.suggestion }}
                </div>
              </div>
            </div>
          </div>

          <div class="optimization-section">
            <h3>{{ $t('pages.mockInterview.report.optimization') }}</h3>
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
            {{ $t('pages.mockInterview.report.saveReport') }}
          </button>
          <button class="action-btn" @click="newInterview">
            <span class="action-icon">🔄</span>
            {{ $t('pages.mockInterview.report.restart') }}
          </button>
          <router-link to="/" class="action-btn">
            <span class="action-icon">🏠</span>
            {{ $t('pages.mockInterview.report.backHome') }}
          </router-link>
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
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import apiClient from '@/utils/api.js'
import ErrorMessage from '@/components/ErrorMessage.vue'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import { trackEvent } from '@/utils/analytics'

const router = useRouter()
const { t, locale } = useI18n()

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

const isInterviewStarted = ref(false)
const isPaused = ref(false)
const isRecording = ref(false)
const showReport = ref(false)
const selectedStyle = ref(t('pages.mockInterview.styles.gentle.name'))
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
const loadingMessage = ref(t('loading.processing'))
const interviewId = ref(null)
const isEnding = ref(false)
let timer = null

const interviewerStyles = computed(() => [
  { name: t('pages.mockInterview.styles.gentle.name'), icon: '😊', description: t('pages.mockInterview.styles.gentle.desc') },
  { name: t('pages.mockInterview.styles.strict.name'), icon: '😐', description: t('pages.mockInterview.styles.strict.desc') },
  { name: t('pages.mockInterview.styles.balanced.name'), icon: '🤔', description: t('pages.mockInterview.styles.balanced.desc') }
])

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

// 规范化面试官风格名称（用于跨语言比较）
const normalizeStyleName = (style) => {
  const styleMap = {
    '温柔HR': '温柔HR',
    '严厉技术总监': '严厉技术总监',
    '综合面试官': '综合面试官',
    'Gentle HR': '温柔HR',
    'Strict Technical Director': '严厉技术总监',
    'Balanced Interviewer': '综合面试官'
  }
  return styleMap[style] || style
}

// 监听语言变化，重置选中的风格和时长
watch(locale, () => {
  selectedStyle.value = t('pages.mockInterview.styles.gentle.name')
  selectedDuration.value = 15
})

const startInterview = async () => {
  // 直接开始面试，不再根据模式检测设备
  await startInterviewProcess()
}

// 实际开始面试的处理函数
const startInterviewProcess = async () => {
  isLoading.value = true
  loadingMessage.value = t('loading.preparingInterview')
  showReport.value = false // 开始面试时隐藏报告
  
  // 从localStorage获取userId
  const userId = localStorage.getItem('userId') || ''
  
  try {
    // 调用后端API开始面试
    const response = await apiClient.post('/mock-interview/start', {
      userId: userId,
      style: selectedStyle.value,
      duration: selectedDuration.value
    })
    
    const data = response.data
    // Track start interview event
    trackEvent('start_interview', {
      style: selectedStyle.value,
      duration: selectedDuration.value
    })

    interviewId.value = data.interviewId
    isInterviewStarted.value = true
    remainingTime.value = selectedDuration.value
    messages.value = [
      {
        sender: 'ai',
        text: t('pages.mockInterview.chat.openingGreeting', { 
          duration: selectedDuration.value, 
          style: selectedStyle.value, 
          question: data.currentQuestion.content 
        }),
        time: getCurrentTime()
      }
    ]
    askedQuestions.value = [data.currentQuestion.content]
    realTimeTips.value = data.tips
    startTimer()
  } catch (error) {
    console.error('开始面试失败:', error)
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
      showErrorMessage(t('alerts.startInterviewFailed'), t('alerts.title'))
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
  loadingMessage.value = t('loading.generatingReport')
  
  // 从localStorage获取userId
  const userId = localStorage.getItem('userId') || ''
  
  // 调用后端API结束面试，获取报告
  apiClient.post('/mock-interview/end', {
    interviewId: interviewId.value,
    userId: userId,
    style: selectedStyle.value,
    duration: selectedDuration.value
  })
  .then(response => {
    // Track end interview event
    trackEvent('end_interview', {
      interview_id: interviewId.value,
      duration_actual: selectedDuration.value - remainingTime.value
    })

    reportData.value = response.data
    showReport.value = true
    isInterviewStarted.value = false
    clearInterval(timer)
    
  })
  .catch(error => {
    console.error('结束面试失败:', error)
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else {
      showErrorMessage(t('alerts.endInterviewFailed'), t('alerts.title'))
    }
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
  loadingMessage.value = t('loading.analyzingAnswer')
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
  apiClient.post('/mock-interview/answer', {
    interviewId: interviewId.value,
    questionId: currentQuestion.value,
    answer: userAnswer
  })
  .then(response => {
    const data = response.data
    
    // 添加AI消息
    messages.value.push({
      sender: 'ai',
      text: t('pages.mockInterview.chat.feedbackTemplate', { 
        feedback: data.feedback, 
        nextQuestion: data.nextQuestion.content 
      }),
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
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else {
      showErrorMessage(t('alerts.answerFailed'), t('alerts.title'))
    }
  })
  .finally(() => {
    isLoading.value = false
  })
}

// 语音识别相关变量（使用MediaRecorder API）
let mediaRecorder = null
let audioStream = null
let audioChunks = []
let isSpeechSupported = ref(true)
// 添加录音状态指示
const recordingStatus = ref('idle') // idle, recording, processing, completed
// 保存当前录音的临时文本，用于追加功能
let currentRecordingText = ''
// 保存当前音频流的时间戳
let currentChunkIndex = 0
// 保存MediaRecorder实例和定时器
let recordTimer = null

// 初始化语音识别（使用MediaRecorder API）
const initSpeechRecognition = () => {
  // 检查浏览器是否支持MediaRecorder
  if (!navigator.mediaDevices || !window.MediaRecorder) {
    isSpeechSupported.value = false
    console.error('浏览器不支持MediaRecorder API')
    realTimeTips.value.push(t('alerts.browserNoMediaRecorder'))
    return
  }
  
  // 明确设置为支持
  isSpeechSupported.value = true
  console.log('MediaRecorder API 初始化完成，浏览器支持语音识别功能')
}

// 将AudioBuffer转换为WAV格式
const audioBufferToWav = (buffer) => {
  // 确保是单声道
  const numOfChan = 1
  const sampleRate = buffer.sampleRate
  const length = buffer.length * numOfChan * 2
  
  // 创建WAV文件头部
  const bufferArray = new ArrayBuffer(44 + length)
  const view = new DataView(bufferArray)
  
  // 写入WAV头信息
  let pos = 0
  
  // RIFF标识符
  writeString(view, pos, 'RIFF')
  pos += 4
  // 文件长度
  view.setUint32(pos, 36 + length, true)
  pos += 4
  // WAVE标识符
  writeString(view, pos, 'WAVE')
  pos += 4
  // fmt子chunk标识符
  writeString(view, pos, 'fmt ')
  pos += 4
  // fmt子chunk长度
  view.setUint32(pos, 16, true)
  pos += 4
  // 音频格式（PCM）
  view.setUint16(pos, 1, true)
  pos += 2
  // 声道数
  view.setUint16(pos, numOfChan, true)
  pos += 2
  // 采样率
  view.setUint32(pos, sampleRate, true)
  pos += 4
  // 字节率 = 采样率 * 声道数 * 采样位深 / 8
  view.setUint32(pos, sampleRate * numOfChan * 2, true)
  pos += 4
  // 块对齐 = 声道数 * 采样位深 / 8
  view.setUint16(pos, numOfChan * 2, true)
  pos += 2
  // 采样位深
  view.setUint16(pos, 16, true)
  pos += 2
  // data子chunk标识符
  writeString(view, pos, 'data')
  pos += 4
  // data子chunk长度
  view.setUint32(pos, length, true)
  pos += 4
  
  // 准备音频数据，确保是单声道
  let channelData
  if (buffer.numberOfChannels > 1) {
    // 转换为单声道：取左右声道的平均值
    const leftChannel = buffer.getChannelData(0)
    const rightChannel = buffer.getChannelData(1)
    channelData = new Float32Array(leftChannel.length)
    for (let i = 0; i < leftChannel.length; i++) {
      channelData[i] = (leftChannel[i] + rightChannel[i]) / 2
    }
  } else {
    // 已经是单声道，直接使用
    channelData = buffer.getChannelData(0)
  }
  
  // 写入音频数据
  for (let i = 0; i < channelData.length; i++) {
    // 将float32转换为int16
    const sample = Math.max(-1, Math.min(1, channelData[i]))
    const intSample = sample < 0 ? sample * 0x8000 : sample * 0x7FFF
    view.setInt16(pos, intSample, true)
    pos += 2
  }
  
  return new Blob([bufferArray], { type: 'audio/wav' })
}

// 辅助函数：写入字符串到DataView
function writeString(view, offset, string) {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i))
  }
}

// 将WebM格式转换为WAV格式
const convertWebMToWav = async (webmBlob) => {
  return new Promise((resolve, reject) => {
    // 创建AudioContext，使用默认采样率
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    
    // 创建FileReader读取WebM文件
    const reader = new FileReader()
    
    reader.onload = async (e) => {
      try {
        // 解码WebM音频数据
        const arrayBuffer = e.target.result
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)
        
        // 如果采样率不是16kHz，进行重采样
        if (audioBuffer.sampleRate !== 16000) {
          console.log(`[DEBUG] 重采样: ${audioBuffer.sampleRate} -> 16000`)
          
          // 创建OfflineAudioContext进行重采样
          const offlineContext = new OfflineAudioContext(
            1, // 单声道
            Math.ceil(audioBuffer.length * (16000 / audioBuffer.sampleRate)),
            16000
          )
          
          // 创建源节点并连接到目标
          const source = offlineContext.createBufferSource()
          source.buffer = audioBuffer
          source.connect(offlineContext.destination)
          
          // 开始渲染
          source.start(0)
          const resampledBuffer = await offlineContext.startRendering()
          
          // 转换为WAV格式
          const wavBlob = audioBufferToWav(resampledBuffer)
          resolve(wavBlob)
        } else {
          // 采样率已经是16kHz，直接转换
          const wavBlob = audioBufferToWav(audioBuffer)
          resolve(wavBlob)
        }
      } catch (error) {
        console.error('[ERROR] 音频转换失败:', error)
        reject(error)
      }
    }
    
    reader.onerror = (error) => {
      console.error('[ERROR] 读取音频文件失败:', error)
      reject(error)
    }
    
    // 开始读取文件
    reader.readAsArrayBuffer(webmBlob)
  })
}

// 发送音频片段到后端
const sendAudioChunk = async (audioBlob, chunkIndex) => {
  const maxRetries = 3
  let retries = 0
  
  while (retries < maxRetries) {
    try {
      const formData = new FormData()
      formData.append('interviewId', interviewId.value)
      formData.append('questionId', currentQuestion.value)
      formData.append('chunkIndex', chunkIndex)
      // 设置语音识别引擎为阿里云ASR
      formData.append('engine', 'aliyun')
      // 使用正确的wav扩展名，因为我们生成的是WAV格式
      formData.append('audio', audioBlob, `chunk_${chunkIndex}.wav`)
      
      const response = await apiClient.post('/mock-interview/realtime-voice', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      const data = response.data
      if (data.status === 'success' && data.transcribedText) {
        // 更新当前录音文本
        currentRecordingText += data.transcribedText
        inputMessage.value = currentRecordingText
        
        // 确保输入框自动滚动到底部
        const textarea = document.querySelector('textarea')
        if (textarea) {
          textarea.scrollTop = textarea.scrollHeight
        }
      }
      
      return data
    } catch (error) {
      retries++
      if (retries >= maxRetries) {
        console.error(`音频片段发送失败，已重试${maxRetries}次:`, error)
        realTimeTips.value.push(t('alerts.networkUnstable'))
        throw error
      }
      
      // 指数退避
      const delay = 1000 * Math.pow(2, retries - 1)
      console.log(`音频片段发送失败，${delay}ms后重试...`)
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
}

// 使用AudioContext和ScriptProcessorNode录制音频，确保生成完整的WAV格式
const handleAudioRecording = () => {
  let audioContext = null
  let scriptProcessor = null
  let mediaStreamSource = null
  let audioBuffer = []
  let sampleRate = 16000
  
  // 初始化AudioContext
  const initAudioContext = () => {
    audioContext = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate: sampleRate
    })
    
    // 创建ScriptProcessorNode，缓冲区大小为4096，1个输入通道，1个输出通道
    scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1)
    
    // 连接麦克风到ScriptProcessorNode
    mediaStreamSource = audioContext.createMediaStreamSource(audioStream)
    mediaStreamSource.connect(scriptProcessor)
    
    // 连接ScriptProcessorNode到输出（扬声器），否则会出现延迟
    scriptProcessor.connect(audioContext.destination)
    
    // 处理音频数据
    scriptProcessor.onaudioprocess = (event) => {
      // 获取输入缓冲区数据
      const inputData = event.inputBuffer.getChannelData(0)
      // 将数据复制到音频缓冲区
      audioBuffer.push(...inputData)
    }
  }
  
  // 开始录音
  const start = () => {
    audioBuffer = []
    initAudioContext()
  }
  
  // 停止录音并获取WAV格式的音频数据
  const stop = () => {
    // 停止ScriptProcessorNode
    scriptProcessor.disconnect()
    mediaStreamSource.disconnect()
    audioContext.close()
    
    // 转换为WAV格式
    const wavBlob = bufferToWave(audioBuffer, sampleRate)
    return wavBlob
  }
  
  // 将音频缓冲区转换为WAV格式
  const bufferToWave = (buffer, sampleRate) => {
    const numOfChan = 1
    const length = buffer.length * numOfChan * 2
    const bufferArray = new ArrayBuffer(length)
    const view = new DataView(bufferArray)
    let offset = 0
    let pos = 0
    
    // 写入WAV头信息
    const setUint16 = (data) => {
      view.setUint16(pos, data, true)
      pos += 2
    }
    
    const setUint32 = (data) => {
      view.setUint32(pos, data, true)
      pos += 4
    }
    
    // RIFF identifier
    setUint32(0x46464952)
    // file length
    setUint32(length + 36)
    // RIFF type
    setUint32(0x45564157)
    // format chunk identifier
    setUint32(0x20746d66)
    // format chunk length
    setUint32(16)
    // sample format (raw)
    setUint16(1)
    // channel count
    setUint16(numOfChan)
    // sample rate
    setUint32(sampleRate)
    // byte rate (sample rate * block align)
    setUint32(sampleRate * numOfChan * 2)
    // block align (channel count * bytes per sample)
    setUint16(numOfChan * 2)
    // bits per sample
    setUint16(16)
    // data chunk identifier
    setUint32(0x61746164)
    // data chunk length
    setUint32(length)
    
    // 写入音频数据
    while (pos < length) {
      let sample = Math.max(-1, Math.min(1, buffer[offset]))
      sample = sample < 0 ? sample * 0x8000 : sample * 0x7FFF
      view.setInt16(pos, sample, true)
      pos += 2
      offset++
    }
    
    return new Blob([bufferArray], { type: 'audio/wav' })
  }
  
  return { start, stop }
}

// 开始录音
const startRecording = async () => {
  try {
    // 请求麦克风权限
    audioStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
        sampleRate: 16000,
        sampleSize: 16,
        channelCount: 1
      }
    })
    
    // 保存当前输入框内容，用于后续追加
    currentRecordingText = inputMessage.value
    currentChunkIndex = 0
    
    // 使用MediaRecorder API进行录音，更可靠且现代
    const mediaRecorder = new MediaRecorder(audioStream, {
      mimeType: 'audio/webm;codecs=opus'
    })
    
    // 音频数据数组
    let chunks = []
    
    // 监听数据可用事件
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunks.push(event.data)
      }
    }
    
    // 监听录制结束事件
    mediaRecorder.onstop = async () => {
      try {
        // 检查是否有实际录音内容（如果chunks为空或只有很小的数据块，说明用户没说话）
        if (chunks.length === 0 || chunks.every(chunk => chunk.size < 100)) {
          console.log('[DEBUG] 录音内容为空，跳过处理')
          recordingStatus.value = 'completed'
          realTimeTips.value.push(t('pages.mockInterview.chat.tips.recordingCompletedNoContent'))
          return
        }
        
        // 合并音频数据
        const webmBlob = new Blob(chunks, { type: 'audio/webm' })
        console.log(`[DEBUG] 生成WebM音频，大小: ${webmBlob.size} bytes，类型: ${webmBlob.type}`)
        
        // 如果WebM音频太小，说明用户没说话
        if (webmBlob.size < 200) {
          console.log('[DEBUG] WebM音频太小，跳过处理')
          recordingStatus.value = 'completed'
          realTimeTips.value.push('✅ 录音已完成（无内容）')
          return
        }
        
        // 转换为WAV格式
        const wavBlob = await convertWebMToWav(webmBlob)
        console.log(`[DEBUG] 转换为WAV音频，大小: ${wavBlob.size} bytes，类型: ${wavBlob.type}`)
        
        // 只发送有实际内容的音频块（WAV头大小为44字节，确保有音频数据）
        if (wavBlob.size > 50) { 
          // 发送音频块到后端
          recordingStatus.value = 'processing'
          await sendAudioChunk(wavBlob, currentChunkIndex)
          currentChunkIndex++
        } else {
          console.log('[DEBUG] WAV音频太小，跳过发送到后端')
        }
        // 录音已完成，设置状态为completed
        recordingStatus.value = 'completed'
      } catch (error) {
        console.error('处理音频数据失败:', error)
        realTimeTips.value.push(t('pages.mockInterview.chat.tips.audioProcessingFailed', { error: error.message }))
        // 出错时也设置为completed状态
        recordingStatus.value = 'completed'
      }
    }
    
    // 开始录音，每1秒触发一次数据可用事件
    mediaRecorder.start(1000)
    
    console.log('录音已开始')
    recordingStatus.value = 'recording'
    realTimeTips.value.push(t('pages.mockInterview.chat.tips.recording'))
    
    // 保存MediaRecorder实例，用于停止录音
    window.currentMediaRecorder = mediaRecorder
  } catch (error) {
    console.error('开始录音失败:', error)
    let errorMessage = '无法访问麦克风设备，请检查权限设置'
    
    if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
      errorMessage = '麦克风权限被拒绝，请在浏览器设置中允许麦克风访问'
      showErrorMessage('麦克风权限被拒绝，请在浏览器设置中允许麦克风访问后重试', '提示')
    } else if (error.name === 'NotFoundError' || error.message.includes('No device found')) {
      errorMessage = '未检测到麦克风设备，请连接麦克风后重试'
    } else if (error.name === 'NotReadableError') {
      errorMessage = '麦克风设备被占用，请关闭其他使用麦克风的应用'
    } else if (error.name === 'OverconstrainedError') {
      errorMessage = '无法满足录音设备要求，请尝试调整麦克风设置'
    } else if (error.name === 'AbortError') {
      errorMessage = '录音已被取消'
    } else {
      // 移动端特殊处理：更友好的错误提示
      const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
      if (isMobile) {
        errorMessage = '录音启动失败，请重试。建议使用Chrome浏览器获得最佳体验'
      }
    }
    
    realTimeTips.value.push(`❌ ${errorMessage}`)
    isRecording.value = false
    recordingStatus.value = 'idle'
  }
}

// 停止录音
const stopRecording = () => {
  // 停止MediaRecorder实例
  if (window.currentMediaRecorder && window.currentMediaRecorder.state !== 'inactive') {
    window.currentMediaRecorder.stop()
    window.currentMediaRecorder = null
  }
  
  // 停止音频流
  if (audioStream) {
    audioStream.getTracks().forEach(track => track.stop())
    audioStream = null
  }
  
  recordingStatus.value = 'completed'
  realTimeTips.value.push(t('pages.mockInterview.chat.tips.recordingCompleted'))
  
  // 1秒后恢复空闲状态
  setTimeout(() => {
    recordingStatus.value = 'idle'
  }, 1000)
}

// 在组件挂载时初始化语音识别
onMounted(async () => {
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
  
  // 在组件挂载时请求麦克风权限，避免每次录音都请求
  // 注意：权限失败不代表浏览器不支持，只是用户拒绝了权限
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
        sampleRate: 44100,
        sampleSize: 16,
        channelCount: 1
      } 
    })
    // 停止临时流，只是为了获取权限
    stream.getTracks().forEach(track => track.stop())
    console.log('麦克风权限已获取')
  } catch (error) {
    console.warn('获取麦克风权限失败:', error)
    // 不要设置 isSpeechSupported.value = false，因为这只是权限问题，不是浏览器支持问题
    // 权限相关的错误会在 startRecording 函数中处理
    if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
      console.log('用户拒绝了麦克风权限，但浏览器仍然支持录音功能')
      realTimeTips.value.push(t('pages.mockInterview.chat.tips.micPermissionNotGranted'))
    } else {
      realTimeTips.value.push(t('pages.mockInterview.chat.tips.micInitHint'))
    }
  }
})

// 组件卸载时停止录音
onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
  stopRecording()
})

const toggleRecording = async () => {
  if (!isSpeechSupported.value) {
    showErrorMessage('您的浏览器不支持语音识别功能，请使用Chrome或Edge等现代浏览器', '提示')
    return
  }
  
  if (isRecording.value) {
    // 停止录音
    console.log('停止录音...')
    isRecording.value = false
    stopRecording()
  } else {
    // 开始录音
    console.log('开始录音...')
    isRecording.value = true
    recordingStatus.value = 'starting'
    realTimeTips.value.push(t('pages.mockInterview.chat.tips.preparing'))
    await startRecording()
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
    showErrorMessage('生成PDF失败，请重试', '失败')
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
    const response = await apiClient.get(`/mock-interview/history`, {
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
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage('请先登录', '提示', () => {
        router.push('/login')
      })
    } else if (error.response && error.response.data.error === 'User not found') {
      showErrorMessage('请先上传简历进行优化，然后再开始模拟面试', '提示', () => {
        router.push('/resume')
      })
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
  
  // 检查返回的记录是否与当前选择的设置匹配（使用规范化后的名称进行比较）
  if (normalizeStyleName(matchingHistory.style) === normalizeStyleName(selectedStyle.value) && 
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

.setup-card, .interview-main-section, .report-card {
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

.report-section {
  width: 100%;
  box-sizing: border-box;
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

/* 平板设备优化 */
@media (min-width: 769px) and (max-width: 1024px) {
  .interview-content {
    grid-template-columns: 1.5fr 1fr;
    gap: 20px;
  }
  
  .setup-card, .interview-main-section, .report-card {
    padding: 25px;
  }
}

/* 移动设备优化 */
@media (max-width: 768px) {
  .mock-interview-container {
    padding: 10px;
  }
  
  .mock-interview-container h1 {
    font-size: 2rem;
  }
  
  .setup-card, .interview-main-section, .report-card {
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
  
  .interview-header, .interview-info, .interview-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
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