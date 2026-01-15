<template>
  <div class="self-intro-container">
    <h1>{{ $t('pages.selfIntro.title') }}</h1>
    
    <!-- 生成中遮盖层 -->
    <div v-if="isGenerating" class="generating-overlay">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <h3>{{ t('loading.generatingIntro') }}</h3>
        <p>{{ t('loading.generatingIntroDesc') }}</p>
      </div>
    </div>
    
    <div class="intro-generation-section">
      <div class="generation-card">
        <h2>{{ $t('pages.selfIntro.desc') }}</h2>
        
        <div class="intro-options">
          <div class="option-group">
            <label>{{ $t('pages.selfIntro.version.label') }}</label>
            <div class="option-buttons">
              <button 
                v-for="version in introVersions" 
                :key="version.length" 
                :class="['option-btn', { active: selectedVersion === version.length }]" 
                @click="selectedVersion = version.length"
              >
                <span class="version-length">{{ version.length }}</span>
                <span class="version-desc">{{ version.desc }}</span>
              </button>
            </div>
          </div>

          <div class="option-group">
            <label>{{ $t('pages.selfIntro.style.label') }}</label>
            <div class="option-buttons">
              <button 
                v-for="style in languageStyles" 
                :key="style" 
                :class="['option-btn', { active: selectedStyle === style }]" 
                @click="selectedStyle = style"
              >
                {{ style }}
              </button>
            </div>
          </div>

          <button class="generate-btn" @click="generateIntro">
            <span class="btn-icon">✨</span>
            {{ $t('pages.selfIntro.generate') }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="generatedIntro" class="intro-result-section">
      <h2>{{ $t('pages.selfIntro.preview') }}</h2>
      
      <div class="result-header">
        <div class="version-info">
          <span class="version-badge">{{ selectedVersion }}</span>
          <span class="style-badge">{{ selectedStyle }}</span>
          <span class="time-estimate">{{ $t('pages.selfIntro.estimatedTime') }}: {{ estimatedTime }}分钟</span>
        </div>
        <div class="result-actions">
          <button class="action-btn" @click="copyIntro">
            <span class="action-icon">📋</span>
            {{ $t('pages.selfIntro.export.copy') }}
          </button>
          <button class="action-btn" @click="toggleTeleprompter">
            <span class="action-icon">📝</span>
            {{ isTeleprompter ? $t('pages.selfIntro.teleprompter.exit') : $t('pages.selfIntro.teleprompter.enter') }}
          </button>
          <button class="action-btn" @click="exportToPDF">
            <span class="action-icon">📄</span>
            {{ $t('pages.selfIntro.export.pdf') }}
          </button>
          <button class="action-btn" @click="regenerateIntro">
            <span class="action-icon">🔄</span>
            {{ $t('pages.selfIntro.regenerate') }}
          </button>
        </div>
      </div>

      <div v-if="!isTeleprompter" class="intro-content">
        <div class="intro-text" ref="introTextRef">
          {{ generatedIntro }}
        </div>
        
        <div class="speech-controls">
          <h3>{{ $t('pages.selfIntro.speechReading') }}</h3>
          <div class="control-buttons">
            <button class="control-btn" @click="togglePlay">
              <span class="control-icon">{{ isPlaying ? '⏸️' : '▶️' }}</span>
              {{ isPlaying ? $t('pages.selfIntro.player.pause') : $t('pages.selfIntro.player.play') }}
            </button>
            <div class="speed-control">
              <label>{{ $t('pages.selfIntro.player.speed') }}:</label>
              <select v-model="playbackSpeed">
                <option value="0.5">0.5x</option>
                <option value="0.75">0.75x</option>
                <option value="1">1x</option>
                <option value="1.25">1.25x</option>
                <option value="1.5">1.5x</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="teleprompter-mode">
        <div class="teleprompter-controls">
          <div class="control-group">
            <label>{{ $t('pages.selfIntro.teleprompter.speedAdjust') }}:</label>
            <input 
              type="range" 
              v-model="teleprompterSpeed" 
              min="1" 
              max="10" 
              step="1"
            />
            <span>{{ teleprompterSpeed }}{{ $t('pages.selfIntro.teleprompter.level') }}</span>
          </div>
          <div class="control-group">
            <label>{{ $t('pages.selfIntro.teleprompter.fontSize') }}:</label>
            <select v-model="fontSize">
              <option value="16">{{ $t('pages.selfIntro.teleprompter.sizes.small') }}</option>
              <option value="20">{{ $t('pages.selfIntro.teleprompter.sizes.medium') }}</option>
              <option value="24">{{ $t('pages.selfIntro.teleprompter.sizes.large') }}</option>
              <option value="28">{{ $t('pages.selfIntro.teleprompter.sizes.xlarge') }}</option>
            </select>
          </div>
          <div class="control-group">
            <label>{{ $t('pages.selfIntro.teleprompter.bgColor') }}:</label>
            <div class="color-options">
              <div 
                v-for="color in bgColors" 
                :key="color.value" 
                class="color-option" 
                :class="{ active: bgColor === color.value }"
                :style="{ backgroundColor: color.value }"
                @click="bgColor = color.value"
              ></div>
            </div>
          </div>
          <button class="control-btn" @click="toggleTeleprompterPlay">
            <span class="control-icon">{{ isTeleprompterPlaying ? '⏸️' : '▶️' }}</span>
            {{ isTeleprompterPlaying ? $t('pages.selfIntro.teleprompter.pause') : $t('pages.selfIntro.teleprompter.start') }}
          </button>
        </div>

        <div class="teleprompter-content" :style="{ fontSize: fontSize + 'px', backgroundColor: bgColor }">
          <div class="teleprompter-text" ref="teleprompterText">
            {{ generatedIntro }}
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
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import ErrorMessage from '@/components/ErrorMessage.vue'
import apiClient from '@/utils/api.js'
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

const selectedVersion = ref(t('pages.selfIntro.version.elevator'))
const selectedStyle = ref(t('pages.selfIntro.style.formal'))
const generatedIntro = ref('')
const isTeleprompter = ref(false)
const isPlaying = ref(false)
const playbackSpeed = ref('1')
const isTeleprompterPlaying = ref(false)
const teleprompterSpeed = ref(5)
const fontSize = ref('20')
const bgColor = ref('#000000')
const teleprompterText = ref(null)
const isGenerating = ref(false)
const estimatedTime = ref('0.5') // 添加estimatedTime的ref，用于接收后端返回的值
const introTextRef = ref(null)

// 页面加载时自动获取已保存的自我介绍
onMounted(async () => {
  try {
    // 从localStorage获取userId，如果没有则生成一个新的
    let userId = localStorage.getItem('userId')
    if (!userId) {
      userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      localStorage.setItem('userId', userId)
    }
    
    // 调用后端API获取已有的自我介绍数据
    await fetchSelfIntro()
  } catch (error) {
    // 如果没有找到数据或其他错误，忽略，等待用户生成
    console.log('没有找到已保存的自我介绍数据，或获取失败:', error)
  }
})

// 监听语言变化，重置选中的版本和风格
watch(locale, () => {
  selectedVersion.value = t('pages.selfIntro.version.elevator')
  selectedStyle.value = t('pages.selfIntro.style.formal')
})

// 根据选择的版本和风格获取自我介绍
const fetchSelfIntro = async () => {
  try {
    let userId = localStorage.getItem('userId')
    if (!userId) return
    
    // 构造introType：版本_风格
    const introType = `${selectedVersion.value}_${selectedStyle.value}`
    
    // 调用后端API获取对应的自我介绍数据
    const response = await apiClient.post('/self-intro/get', {
      userId: userId,
      introType: introType
    })
    
    // 如果返回了自我介绍数据，填充到页面上
    if (response.data && response.data.intro) {
      generatedIntro.value = response.data.intro
      estimatedTime.value = response.data.estimatedTime
    } else {
      // 如果没有找到对应类型的数据，清空显示
      generatedIntro.value = ''
    }
  } catch (error) {
    console.log('获取特定类型自我介绍失败:', error)
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else if (error.response && error.response.data && error.response.data.error === 'User not found') {
      showErrorMessage(t('alerts.uploadResumeFirst'), t('alerts.title'), () => {
        router.push('/resume')
      })
    } else {
      generatedIntro.value = ''
    }
  }
}

// 监听版本长度和语言风格的变化，自动获取对应的数据
watch([selectedVersion, selectedStyle], () => {
  fetchSelfIntro()
})

const introVersions = computed(() => [
  { length: t('pages.selfIntro.version.elevator'), desc: t('pages.selfIntro.version.elevatorDesc') },
  { length: t('pages.selfIntro.version.standard'), desc: t('pages.selfIntro.version.standardDesc') },
  { length: t('pages.selfIntro.version.detailed'), desc: t('pages.selfIntro.version.detailedDesc') }
])

const languageStyles = computed(() => [
  t('pages.selfIntro.style.formal'),
  t('pages.selfIntro.style.casual'),
  t('pages.selfIntro.style.academic')
])

const bgColors = [
  { value: '#000000' },
  { value: '#1a1a1a' },
  { value: '#2d2d2d' },
  { value: '#404040' }
]



const generateIntro = () => {
  isGenerating.value = true
  
  // 从localStorage获取userId，如果没有则生成一个新的
  let userId = localStorage.getItem('userId')
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    localStorage.setItem('userId', userId)
  }
  
  // 调用后端API，只传递userId，不传递resumeId
  apiClient.post('/self-intro/generate', {
    version: selectedVersion.value,
    style: selectedStyle.value,
    userId: userId
  })
  .then(response => {
    generatedIntro.value = response.data.intro
    estimatedTime.value = response.data.estimatedTime
    
    // Track generate self intro event
    trackEvent('generate_self_intro', {
      version: selectedVersion.value,
      style: selectedStyle.value
    })
    // 保存userId到localStorage，确保后续请求使用相同的userId
    if (response.data.userId) {
      localStorage.setItem('userId', response.data.userId)
    }
  })
  .catch(error => {
    console.error('生成自我介绍失败:', error)
    if (error.isUnauthorized) {
      // 401错误，显示请先登录提示，点击确定后跳转到登录页
      showErrorMessage(t('alerts.loginRequired'), t('alerts.title'), () => {
        router.push('/login')
      })
    } else {
      showErrorMessage(t('alerts.generateIntroFailed'), t('alerts.title'))
    }
  })
  .finally(() => {
    isGenerating.value = false
  })
}

const copyIntro = () => {
  navigator.clipboard.writeText(generatedIntro.value)
  showErrorMessage(t('alerts.copied'), t('alerts.title'))
}

const toggleTeleprompter = () => {
  isTeleprompter.value = !isTeleprompter.value
  if (!isTeleprompter.value) {
    isTeleprompterPlaying.value = false
  }
}

const regenerateIntro = () => {
  generateIntro()
}

// 创建语音合成器实例
const speechSynthesis = window.speechSynthesis

// 监听语速变化，实时更新语音合成器的语速
watch(playbackSpeed, (newSpeed) => {
  // 语速变化时，如果正在播放，需要重新开始播放以应用新速度
  if (isPlaying.value) {
    // 停止当前播放
    speechSynthesis.cancel()
    // 重新开始播放
    playIntro()
  }
})

// 播放自我介绍
const playIntro = () => {
  if (!generatedIntro.value) return
  
  // 检查浏览器是否支持语音合成
  if (!window.speechSynthesis) {
    showErrorMessage(t('alerts.browserNoSpeechSynthesis'), t('alerts.title'))
    return
  }
  
  try {
    // 每次播放都创建新的utterance实例，避免多次播放同一个utterance的问题
    const utterance = new SpeechSynthesisUtterance()
    
    // 设置语音合成参数
    utterance.text = generatedIntro.value
    utterance.lang = 'zh-CN' // 中文
    utterance.rate = parseFloat(playbackSpeed.value) // 播放速度
    utterance.pitch = 1 // 音调
    utterance.volume = 1 // 音量
    
    // 开始播放
    speechSynthesis.speak(utterance)
    
    // 播放结束时重置状态
    utterance.onend = () => {
      isPlaying.value = false
    }
    
    // 播放错误处理
    utterance.onerror = (event) => {
      console.error('语音合成错误:', event)
      isPlaying.value = false
      showErrorMessage(t('alerts.speechSynthesisFailed'), t('alerts.title'))
    }
    
  } catch (error) {
    console.error('播放自我介绍失败:', error)
    isPlaying.value = false
    showErrorMessage(t('alerts.playFailed'), t('alerts.title'))
  }
}

const togglePlay = () => {
  if (isPlaying.value) {
    // 暂停播放
    speechSynthesis.pause()
  } else {
    // 开始播放
    playIntro()
  }
  
  isPlaying.value = !isPlaying.value
}

const toggleTeleprompterPlay = () => {
  isTeleprompterPlaying.value = !isTeleprompterPlaying.value
  // 这里可以添加实际的提词器滚动逻辑
}

// 导出PDF功能
const exportToPDF = () => {
  if (!generatedIntro.value || !introTextRef.value) return
  
  // 使用html2canvas和jsPDF结合的方式生成PDF，解决中文乱码问题
  Promise.all([
    import('html2canvas'),
    import('jspdf')
  ]).then(([{ default: html2canvas }, { jsPDF }]) => {
    // 创建一个临时的PDF内容容器
    const pdfContainer = document.createElement('div')
    pdfContainer.style.position = 'fixed'
    pdfContainer.style.top = '-1000px'
    pdfContainer.style.left = '-1000px'
    pdfContainer.style.width = '800px'
    pdfContainer.style.padding = '20px'
    pdfContainer.style.backgroundColor = 'white'
    pdfContainer.style.color = '#333'
    
    // 添加标题
    const title = document.createElement('h1')
    title.textContent = '自我介绍'
    title.style.textAlign = 'center'
    title.style.marginBottom = '20px'
    title.style.fontSize = '24px'
    pdfContainer.appendChild(title)
    
    // 添加版本和风格信息
    const infoContainer = document.createElement('div')
    infoContainer.style.display = 'flex'
    infoContainer.style.justifyContent = 'space-between'
    infoContainer.style.marginBottom = '20px'
    infoContainer.style.paddingBottom = '10px'
    infoContainer.style.borderBottom = '1px solid #ddd'
    
    const versionInfo = document.createElement('div')
    // 确保获取到的是字符串值
    const versionValue = typeof selectedVersion === 'string' ? selectedVersion : selectedVersion.value || '未知版本'
    versionInfo.textContent = `版本：${versionValue}`
    versionInfo.style.fontSize = '14px'
    
    const styleInfo = document.createElement('div')
    // 确保获取到的是字符串值
    const styleValue = typeof selectedStyle === 'string' ? selectedStyle : selectedStyle.value || '未知风格'
    styleInfo.textContent = `风格：${styleValue}`
    styleInfo.style.fontSize = '14px'
    
    const timeInfo = document.createElement('div')
    // 确保获取到的是字符串值
    const timeValue = typeof estimatedTime === 'string' ? estimatedTime : estimatedTime.value || '0'
    timeInfo.textContent = `预计朗读时间：${timeValue}分钟`
    timeInfo.style.fontSize = '14px'
    
    infoContainer.appendChild(versionInfo)
    infoContainer.appendChild(styleInfo)
    infoContainer.appendChild(timeInfo)
    pdfContainer.appendChild(infoContainer)
    
    // 添加自我介绍内容
    const content = document.createElement('div')
    content.textContent = generatedIntro.value
    content.style.fontSize = '16px'
    content.style.lineHeight = '1.8'
    content.style.whiteSpace = 'pre-wrap'
    pdfContainer.appendChild(content)
    
    // 将容器添加到DOM
    document.body.appendChild(pdfContainer)
    
    // 使用html2canvas将内容转换为图片
    html2canvas(pdfContainer, {
      scale: 2, // 提高清晰度
      useCORS: true,
      logging: false
    }).then(canvas => {
      // 计算PDF尺寸
      const imgData = canvas.toDataURL('image/png')
      const imgWidth = 210 // A4宽度，单位mm
      const pageHeight = 297 // A4高度，单位mm
      const imgHeight = canvas.height * imgWidth / canvas.width
      let heightLeft = imgHeight
      let position = 0
      
      // 创建PDF
      const doc = new jsPDF('p', 'mm', 'a4')
      
      // 添加第一张图片
      doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      heightLeft -= pageHeight
      
      // 如果内容超过一页，添加新页
      while (heightLeft > 0) {
        position = heightLeft - imgHeight
        doc.addPage()
        doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
        heightLeft -= pageHeight
      }
      
      // 保存PDF
    // 确保文件名中使用正确的字符串值
    const fileNameVersion = typeof selectedVersion === 'string' ? selectedVersion : selectedVersion.value || '未知版本'
    const fileNameStyle = typeof selectedStyle === 'string' ? selectedStyle : selectedStyle.value || '未知风格'
    doc.save(`自我介绍_${fileNameVersion}_${fileNameStyle}.pdf`)
      
      // 清理临时容器
      document.body.removeChild(pdfContainer)
    })
  })
}
</script>

<style scoped>
.self-intro-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.self-intro-container h1 {
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.intro-generation-section {
  margin-bottom: 40px;
}

.generation-card {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.generation-card h2 {
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.intro-options {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
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
  padding: 12px 20px;
  border: 2px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 150px;
}

.option-btn:hover {
  border-color: #667eea;
}

.option-btn.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.version-length {
  display: block;
  font-weight: bold;
  font-size: 1.1rem;
}

.version-desc {
  display: block;
  font-size: 0.9rem;
  opacity: 0.8;
}

.option-group textarea {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: vertical;
  font-size: 1rem;
  font-family: inherit;
}

.option-group textarea:focus {
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

.intro-result-section {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.intro-result-section h2 {
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
  flex-wrap: wrap;
  gap: 20px;
}

.version-info {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.version-badge, .style-badge {
  padding: 8px 15px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.version-badge {
  background-color: #667eea;
  color: white;
}

.style-badge {
  background-color: #42b883;
  color: white;
}

.time-estimate {
  color: #666;
  font-size: 0.9rem;
}

.result-actions {
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

.intro-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.intro-text {
  background-color: #f8f9fa;
  padding: 30px;
  border-radius: 8px;
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
  text-align: left;
}

.speech-controls {
  background-color: #f0f4ff;
  padding: 20px;
  border-radius: 8px;
}

.speech-controls h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 1.2rem;
}

.control-buttons {
  display: flex;
  gap: 20px;
  align-items: center;
  flex-wrap: wrap;
}

.control-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
}

.control-btn:hover {
  background-color: #5568d3;
  transform: translateY(-2px);
}

.control-icon {
  font-size: 1.1rem;
}

.speed-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.speed-control label {
  font-weight: bold;
  color: #333;
}

.speed-control select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
}

.teleprompter-mode {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.teleprompter-controls {
  background-color: #f0f4ff;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  gap: 20px;
  align-items: center;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.control-group label {
  font-weight: bold;
  color: #333;
  white-space: nowrap;
}

.control-group input[type="range"] {
  flex: 1;
  min-width: 100px;
}

.control-group select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
}

.color-options {
  display: flex;
  gap: 10px;
}

.color-option {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.color-option.active {
  border-color: white;
  box-shadow: 0 0 0 2px #667eea;
}

.teleprompter-content {
  background-color: #000000;
  color: white;
  padding: 50px;
  border-radius: 8px;
  overflow: hidden;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.teleprompter-text {
  text-align: center;
  line-height: 2.5;
  font-weight: bold;
  max-width: 800px;
  animation: scroll linear infinite;
}

@keyframes scroll {
  0% { transform: translateY(100%); }
  100% { transform: translateY(-100%); }
}

/* 生成中遮盖层样式 */
.generating-overlay {
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

.loading-container {
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

.loading-container h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.loading-container p {
  color: #666;
  margin: 0;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .self-intro-container {
    padding: 10px;
  }
  
  .self-intro-container h1 {
    font-size: 2rem;
  }
  
  .generation-card,
  .intro-result-section {
    padding: 20px;
  }
  
  .result-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .version-info {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .result-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .control-buttons {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .teleprompter-controls {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .teleprompter-content {
    padding: 30px 20px;
    min-height: 300px;
  }
  
  .loading-container {
    padding: 30px 20px;
  }
  
  .loading-spinner {
    width: 50px;
    height: 50px;
  }
}
</style>