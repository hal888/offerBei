<template>
  <div class="resume-container">
    <h1>简历解析与智能优化</h1>
    
    <!-- 上传加载遮盖层 -->
    <div v-if="isUploading" class="upload-overlay">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <h3>简历上传中...</h3>
        <p>正在分析您的简历，请稍候</p>
      </div>
    </div>
    
    <div class="resume-upload-section">
      <div class="upload-card">
        <div class="upload-icon"></div>
        <h2>上传您的简历</h2>
        <p>支持 PDF、DOCX、JPG/PNG 格式，单文件 ≤ 10MB</p>
        
        <div class="upload-options">
          <div class="file-input-container">
            <input type="file" id="resume-file" accept=".pdf,.docx,.jpg,.jpeg,.png" @change="handleFileUpload" :disabled="isUploading" />
            <label for="resume-file" class="file-input-label" :class="{ 'disabled': isUploading }">
              <span class="file-icon">📁</span>
              选择文件
            </label>
          </div>
          
          <div class="drag-drop-area" @dragover.prevent @drop.prevent="handleDragDrop" :class="{ 'disabled': isUploading }">
            <span>或拖拽文件到此处</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="resumeData" class="resume-analysis-section">
      <h2>简历分析结果</h2>
      
      <div class="analysis-header">
        <div class="resume-score">
          <h3>简历评分</h3>
          <div class="score-circle">
            <span class="score-value">{{ resumeData.score }}</span>
            <span class="score-max">/100</span>
          </div>
          <p class="score-description">{{ getScoreDescription(resumeData.score) }}</p>
        </div>
      </div>

      <div class="analysis-content">
        <div class="diagnosis-section">
          <h3>智能诊断</h3>
          <div class="diagnosis-list">
            <div v-for="(item, index) in resumeData.diagnosis" :key="index" class="diagnosis-item">
              <div class="diagnosis-type" :class="item.type">{{ item.type }}</div>
              <div class="diagnosis-content">
                <h4>{{ item.title }}</h4>
                <p>{{ item.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="optimization-section">
          <h3>智能优化建议</h3>
          <div class="optimization-tabs">
            <button 
              v-for="tab in optimizationTabs" 
              :key="tab" 
              :class="['tab-btn', { active: activeTab === tab }]" 
              @click="activeTab = tab"
            >
              {{ tab }}
            </button>
          </div>

          <div class="optimization-content">
            <div v-if="activeTab === 'STAR法则重写'" class="star-rewrite">
              <h4>STAR法则优化建议</h4>
              <div v-if="resumeData.starRewrite && resumeData.starRewrite.length > 0" class="star-list">
                <div v-for="(item, index) in resumeData.starRewrite" :key="index" class="star-item optimized">
                  <div class="star-section">
                    <span class="star-label">情境(S)：</span>
                    <span class="star-content">{{ item.situation || '无' }}</span>
                  </div>
                  <div class="star-section">
                    <span class="star-label">任务(T)：</span>
                    <span class="star-content">{{ item.task || '无' }}</span>
                  </div>
                  <div class="star-section">
                    <span class="star-label">行动(A)：</span>
                    <span class="star-content">{{ item.action || '无' }}</span>
                  </div>
                  <div class="star-section">
                    <span class="star-label">结果(R)：</span>
                    <span class="star-content">{{ item.result || '无' }}</span>
                  </div>
                </div>
              </div>
              <div v-else class="star-placeholder">
                <p>暂无STAR法则优化建议</p>
              </div>
            </div>

            <div v-if="activeTab === '关键词注入'" class="keyword-injection">
              <h4>关键词优化建议</h4>
              <div class="keyword-list">
                <div class="keyword-item" v-for="(keyword, index) in resumeData.keywords" :key="index">
                  <span class="keyword">{{ keyword }}</span>
                  <span class="keyword-type">{{ getKeywordType(keyword) }}</span>
                </div>
              </div>
              <p class="keyword-tip">建议在简历中自然融入以上关键词，提升ATS系统匹配度</p>
            </div>
          </div>
        </div>

        <div class="preview-section">
          <h3>优化后简历预览</h3>
          <div class="preview-content">
            <div v-if="resumeData.optimizedResume" class="preview-text">
              <div class="resume-preview" v-html="formattedResume"></div>
            </div>
            <div v-else class="preview-placeholder">
              <span>简历预览区域</span>
            </div>
            <div class="preview-actions">
              <button class="btn primary-btn" @click="downloadResume">下载优化后简历</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { jsPDF } from 'jspdf'
import html2canvas from 'html2canvas'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css' // 导入highlight.js的GitHub样式

const resumeData = ref(null)
const activeTab = ref('STAR法则重写')
const optimizationTabs = ['STAR法则重写', '关键词注入']
const isUploading = ref(false)

// 页面加载时自动获取最新的简历优化内容
onMounted(async () => {
  try {
    // 从localStorage获取userId，如果没有则生成一个新的
    let userId = localStorage.getItem('userId')
    if (!userId) {
      userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      localStorage.setItem('userId', userId)
    }
    
    // 调用后端API获取最新的简历数据
    const response = await axios.post('http://localhost:5000/api/resume/get', {
      userId: userId
    })
    
    // 如果返回了简历数据，填充到页面上
    if (response.data && response.data.optimizedResume) {
      resumeData.value = response.data
      // 保存resumeId到localStorage
      if (response.data.resumeId) {
        localStorage.setItem('resumeId', response.data.resumeId)
      }
    }
  } catch (error) {
    // 如果没有找到数据或其他错误，忽略，等待用户上传新简历
    console.log('获取最新简历失败:', error)
  }
})

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    uploadResume(file)
  }
}

const handleDragDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file) {
    uploadResume(file)
  }
}

const uploadResume = (file) => {
  isUploading.value = true
  
  // 从localStorage获取userId，如果没有则生成一个新的
  let userId = localStorage.getItem('userId')
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    localStorage.setItem('userId', userId)
  }
  
  // 创建FormData对象
  const formData = new FormData()
  formData.append('file', file)
  formData.append('userId', userId) // 添加userId到请求中
  
  // 调用后端API
  axios.post('http://localhost:5000/api/resume/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  .then(response => {
    resumeData.value = response.data
    // 保存resumeId到localStorage
    if (response.data.resumeId) {
      localStorage.setItem('resumeId', response.data.resumeId)
    }
    // 保存userId到localStorage，确保后续请求使用相同的userId
    if (response.data.userId) {
      localStorage.setItem('userId', response.data.userId)
    }
  })
  .catch(error => {
    console.error('简历分析失败:', error)
    alert('简历分析失败，请重试')
  })
  .finally(() => {
    isUploading.value = false
  })
}

const getScoreDescription = (score) => {
  if (score >= 90) return '优秀的简历，具有很强的竞争力'
  if (score >= 80) return '良好的简历，需要一些小的优化'
  if (score >= 70) return '中等的简历，有改进空间'
  if (score >= 60) return '基础的简历，需要较多优化'
  return '较差的简历，建议重新撰写'
}

const getKeywordType = (keyword) => {
  const techKeywords = ['JavaScript', 'Vue', 'React', 'Node.js', 'RESTful API', '数据库设计', '性能优化']
  return techKeywords.includes(keyword) ? '技术关键词' : '软技能关键词'
}

// 配置marked库，使用highlight.js进行代码块语法高亮
marked.setOptions({
  highlight: function(code, lang) {
    // 如果指定了语言且hljs支持该语言，则进行语法高亮
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (__) {}
    }
    // 否则返回原始代码，不进行高亮
    return code
  },
  breaks: true, // 允许换行符转换为<br>
  gfm: true, // 启用GitHub风格的Markdown
  sanitize: true // 启用HTML sanitize，确保安全渲染
})

// 格式化简历内容
const formattedResume = computed(() => {
  if (!resumeData.value?.optimizedResume) return ''
  
  try {
    let resume = resumeData.value.optimizedResume
    
    // 使用marked库解析Markdown为HTML
    return marked(resume)
  } catch (error) {
    console.error('Markdown解析错误:', error)
    return '<p>简历内容解析失败，请稍后重试</p>'
  }
})

// 下载简历功能 - PDF格式
const downloadResume = async () => {
  if (!resumeData.value?.optimizedResume) return
  
  try {
    // 获取简历预览元素
    const resumeElement = document.querySelector('.resume-preview')
    if (!resumeElement) return
    
    // 使用html2canvas将HTML转换为canvas
    const canvas = await html2canvas(resumeElement, {
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
    doc.save('optimized_resume.pdf')
  } catch (error) {
    console.error('生成PDF失败:', error)
    alert('生成PDF失败，请重试')
  }
}


</script>

<style scoped>
.resume-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.resume-container h1 {
  font-size: 2.5rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.resume-upload-section {
  display: flex;
  justify-content: center;
  margin-bottom: 50px;
}

.upload-card {
  background-color: white;
  padding: 60px 40px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 600px;
  width: 100%;
  border: 2px dashed #667eea;
}

.upload-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23667eea"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
}

.upload-card h2 {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: #333;
}

.upload-card p {
  color: #666;
  margin-bottom: 30px;
}

.upload-options {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.file-input-container {
  position: relative;
}

#resume-file {
  display: none;
}

.file-input-label {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  background-color: #667eea;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.file-input-label:hover {
  background-color: #5568d3;
  transform: translateY(-2px);
}

.file-icon {
  font-size: 1.2rem;
}

.drag-drop-area {
  width: 100%;
  padding: 30px;
  border: 2px dashed #ddd;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.drag-drop-area:hover {
  border-color: #667eea;
  background-color: #f0f4ff;
}

.resume-analysis-section {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.resume-analysis-section h2 {
  font-size: 2rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.analysis-header {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.resume-score {
  text-align: center;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: conic-gradient(#667eea 0deg 270deg, #e0e0e0 270deg 360deg);
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 20px;
  position: relative;
}

.score-circle::before {
  content: '';
  position: absolute;
  width: 130px;
  height: 130px;
  border-radius: 50%;
  background-color: white;
}

.score-value {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
  position: relative;
  z-index: 1;
}

.score-max {
  font-size: 1.5rem;
  color: #999;
  position: relative;
  z-index: 1;
}

.score-description {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.diagnosis-section h3,
.optimization-section h3,
.preview-section h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
}

.diagnosis-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.diagnosis-item {
  display: flex;
  gap: 15px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.diagnosis-type {
  font-weight: bold;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  white-space: nowrap;
}

.diagnosis-type.警告 {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
}

.diagnosis-type.错误 {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.diagnosis-type.建议 {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.diagnosis-content h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1.1rem;
}

.diagnosis-content p {
  margin: 0;
  color: #666;
}

.optimization-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-btn {
  padding: 10px 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  border-color: #667eea;
}

.tab-btn.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.optimization-content {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.star-rewrite h4,
.keyword-injection h4 {
  margin-top: 0;
  color: #333;
  font-size: 1.2rem;
}

.star-example {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.star-item {
  padding: 15px;
  background-color: white;
  border-radius: 5px;
  border-left: 4px solid #667eea;
}

.star-item.optimized {
  border-left-color: #42b883;
}

.star-item strong {
  color: #333;
}

.star-label {
  font-weight: bold;
  color: #667eea;
}

.keyword-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.keyword-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  background-color: white;
  border-radius: 20px;
  border: 1px solid #e0e0e0;
}

.keyword {
  font-weight: bold;
  color: #667eea;
}

.keyword-type {
  font-size: 0.8rem;
  color: #999;
}

.keyword-tip {
  color: #666;
  font-style: italic;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preview-placeholder {
  width: 100%;
  height: 400px;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #999;
  border-radius: 5px;
  border: 2px dashed #ddd;
}

.preview-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-start;
}

.btn {
  padding: 12px 25px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.primary-btn {
  background-color: #42b883;
  color: white;
}

.primary-btn:hover {
  background-color: #369f70;
  transform: translateY(-2px);
}

.secondary-btn {
  background-color: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.secondary-btn:hover {
  background-color: #667eea;
  color: white;
  transform: translateY(-2px);
}

/* 上传加载遮盖层样式 */
.upload-overlay {
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

/* 禁用状态样式 */
.file-input-label.disabled,
.drag-drop-area.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.file-input-label.disabled:hover {
  background-color: #667eea;
  transform: none;
}

.drag-drop-area.disabled:hover {
  border-color: #ddd;
  background-color: transparent;
}

/* 简历预览样式 */
.preview-text {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  max-height: 500px;
  overflow-y: auto;
  text-align: left;
}

/* 格式化简历样式 */
.resume-preview {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 1rem !important;
  line-height: 1.6 !important;
  color: #2c3e50 !important;
  background-color: #ffffff !important;
  padding: 40px !important;
  border-radius: 8px !important;
  min-height: 500px !important;
  text-align: left !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
  display: block !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

/* 直接应用样式到marked生成的HTML标签 */
.resume-preview h1,
.resume-preview h2,
.resume-preview h3,
.resume-preview h4,
.resume-preview h5,
.resume-preview h6,
.resume-preview p,
.resume-preview ul,
.resume-preview ol,
.resume-preview li,
.resume-preview pre,
.resume-preview code,
.resume-preview blockquote,
.resume-preview table,
.resume-preview th,
.resume-preview td,
.resume-preview a,
.resume-section,
.resume-subsection,
.resume-item-title {
  text-align: left !important;
  box-sizing: border-box !important;
}

/* 为不同级别标题设置不同的间距，标题前后空1行 */
/* 直接选择所有可能的标题元素，确保样式应用到Markdown生成的标题 */
:deep(.resume-preview h1),
:deep(.resume-section){
  margin: 20x 0 20px 0 !important; /* 标题前后空1行（假设每行20px） */
  font-size: 28px !important;
  font-weight: 700 !important;
  color: #1a202c !important;
  padding-bottom: 12px !important;
  border-bottom: 3px solid #3498db !important;
}

:deep(.resume-preview h2),
:deep(.resume-subsection) {
  margin: 20x 0 20x 0 !important; /* 标题前后空1行 */
  font-size: 22px !important;
  font-weight: 600 !important;
  color: #2d3748 !important;
  padding-left: 15px !important;
  border-left: 4px solid #3498db !important;
}

/* 三级标题样式 */
:deep(.resume-preview h3),
:deep(.resume-item-title) {
  margin: 20px 0 20px 0 !important; /* 标题前后空1行 */
  font-size: 18px !important;
  font-weight: 600 !important;
  color: #4a5568 !important;
  background-color: #f7fafc !important;
  padding: 12px 16px !important;
  border-radius: 6px !important;
  border-left: 4px solid #3498db !important;
}

/* 四级标题样式 */
:deep(.resume-preview h4) {
  margin: 20px 0 20px 0 !important; /* 标题前后空1行 */
  font-size: 16px !important;
  color: #2d3748 !important;
  font-weight: 600 !important;
}

/* 五级和六级标题样式 */
:deep(.resume-preview h5),
:deep(.resume-preview h6) {
  margin: 20px 0 20px 0 !important; /* 标题前后空1行 */
  font-weight: 600 !important;
  color: #4a5568 !important;
}

/* 段落样式 */
.resume-preview p,
.resume-paragraph {
  margin: 20px 0 !important;
  line-height: 2.0 !important;
  color: #4a5568 !important;
  font-size: 15px !important;
  word-spacing: 8px !important;
}

/* 列表样式 */
.resume-preview ul,
.resume-preview ol,
.resume-list {
  margin: 15px 0 15px 25px !important;
  padding-left: 25px !important;
}

.resume-preview li,
.resume-list-item {
  margin: 10px 0 !important;
  list-style-type: disc !important;
  color: #4a5568 !important;
  line-height: 1.8 !important;
}

.resume-preview ol li {
  list-style-type: decimal !important;
}

/* 列表标记样式优化 */
.resume-preview ul li::marker {
  color: #3498db !important;
  font-weight: bold !important;
}

.resume-preview ol li::marker {
  color: #3498db !important;
  font-weight: bold !important;
}



/* 个人信息行特殊处理 */
.resume-preview > p:first-child,
.resume-preview > div:first-child > p:first-child {
  font-size: 18px !important;
  font-weight: 600 !important;
  color: #1a202c !important;
  margin-bottom: 15px !important;
  line-height: 2.2 !important;
  white-space: pre-line !important; /* 保留换行符 */
}

/* 个人联系方式行处理 */
.resume-preview > p:nth-child(2),
.resume-preview > p:nth-child(3),
.resume-preview > div:first-child > p:nth-child(2),
.resume-preview > div:first-child > p:nth-child(3) {
  font-size: 15px !important;
  color: #718096 !important;
  margin-bottom: 15px !important;
  line-height: 2.2 !important;
  white-space: pre-line !important; /* 保留换行符 */
  word-break: break-word !important; /* 长文本自动换行 */
}

/* 移除个人信息项样式，改为更简洁的展示 */
.resume-preview > p:first-child span,
.resume-preview > p:nth-child(2) span,
.resume-preview > p:nth-child(3) span {
  display: inline !important;
  margin-right: 0 !important;
  margin-bottom: 0 !important;
  padding: 0 !important;
  background-color: transparent !important;
  border-radius: 0 !important;
  border-left: none !important;
}

/* 日期样式 */
.resume-preview h4 + p {
  color: #718096 !important;
  font-size: 14px !important;
  margin-top: 0 !important;
  margin-bottom: 12px !important;
  font-style: italic !important;
}

/* 图片样式 */
.resume-preview img {
  max-width: 100% !important;
  height: auto !important;
  display: block !important;
  margin: 20px auto !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

/* 分隔线样式 */
.resume-preview hr {
  border: none !important;
  border-top: 2px solid #e2e8f0 !important;
  margin: 30px 0 !important;
  opacity: 0.7 !important;
}

/* 引用样式 */
.resume-preview blockquote {
  border-left: 4px solid #3498db !important;
  padding: 15px 20px !important;
  margin: 20px 0 !important;
  color: #718096 !important;
  font-style: italic !important;
  background-color: #f7fafc !important;
  border-radius: 0 6px 6px 0 !important;
}

/* 表格样式 */
.resume-preview table {
  border-collapse: collapse !important;
  width: 100% !important;
  margin: 20px 0 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

.resume-preview th,
.resume-preview td {
  border: 1px solid #e2e8f0 !important;
  padding: 12px 15px !important;
  text-align: left !important;
  font-size: 14px !important;
}

.resume-preview th {
  background-color: #f7fafc !important;
  font-weight: 600 !important;
  color: #2d3748 !important;
  border-bottom: 2px solid #e2e8f0 !important;
}

.resume-preview tr:nth-child(even) {
  background-color: #fafafa !important;
}

.resume-preview tr:hover {
  background-color: #f7fafc !important;
}

/* 代码块样式 */
.resume-preview pre {
  background-color: #f7fafc !important;
  padding: 20px !important;
  border-radius: 8px !important;
  overflow-x: auto !important;
  margin: 20px 0 !important;
  font-family: 'SF Mono', 'Roboto Mono', 'Courier New', Courier, monospace !important;
  font-size: 14px !important;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
}

.resume-preview code {
  background-color: #edf2f7 !important;
  padding: 4px 8px !important;
  border-radius: 4px !important;
  font-family: 'SF Mono', 'Roboto Mono', 'Courier New', Courier, monospace !important;
  font-size: 14px !important;
  color: #e53e3e !important;
}

.resume-preview pre code {
  background-color: transparent !important;
  padding: 0 !important;
  border-radius: 0 !important;
  color: #2d3748 !important;
}

/* 任务列表样式 */
.resume-preview ul.contains-task-list {
  list-style-type: none !important;
  padding-left: 0 !important;
  margin-left: 0 !important;
}

.resume-preview .task-list-item {
  display: flex !important;
  align-items: flex-start !important;
  margin: 10px 0 !important;
}

.resume-preview .task-list-item input[type="checkbox"] {
  margin-right: 10px !important;
  margin-top: 6px !important;
  flex-shrink: 0 !important;
}

/* 脚注样式 */
.resume-preview sup {
  font-size: 0.8em !important;
  vertical-align: super !important;
  color: #3498db !important;
}

.resume-preview .footnote-ref {
  text-decoration: none !important;
  border-bottom: none !important;
  color: #3498db !important;
}

.resume-preview .footnote-definition {
  margin: 15px 0 !important;
  padding-left: 25px !important;
  font-size: 14px !important;
  color: #718096 !important;
}



/* 强调样式 */
.resume-preview strong {
  color: #1a202c !important;
  font-weight: 700 !important;
}

.resume-preview em {
  color: #718096 !important;
  font-style: italic !important;
}

/* 链接样式 */
.resume-preview a {
  color: #3498db !important;
  text-decoration: none !important;
  border-bottom: 1px solid #3498db !important;
  transition: all 0.2s ease !important;
}

.resume-preview a:hover {
  color: #2980b9 !important;
  border-bottom: 2px solid #2980b9 !important;
}

.preview-text pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  margin: 0;
}

/* STAR法则重写样式 */
.star-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.star-section {
  margin-bottom: 10px;
  line-height: 1.6;
  display: flex;
  align-items: flex-start;
}

.star-label {
  font-weight: bold;
  color: #667eea;
  width: 80px;
  flex-shrink: 0;
  text-align: right;
  padding-right: 15px;
}

.star-content {
  flex: 1;
  text-align: left;
}

.star-placeholder {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
  color: #999;
  border: 1px dashed #e0e0e0;
}

/* 智能诊断样式优化 */
.diagnosis-item {
  display: flex;
  gap: 15px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  align-items: flex-start;
}

.diagnosis-type {
  font-weight: bold;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 4px;
}

.diagnosis-content {
  flex: 1;
}

@media (max-width: 768px) {
  .resume-container {
    padding: 10px;
  }
  
  .resume-container h1 {
    font-size: 2rem;
  }
  
  .upload-card {
    padding: 40px 20px;
  }
  
  .resume-analysis-section {
    padding: 20px;
  }
  
  .diagnosis-item {
    flex-direction: column;
    gap: 10px;
  }
  
  .diagnosis-type {
    align-self: flex-start;
  }
  
  .preview-placeholder {
    height: 300px;
  }
  
  .preview-actions {
    flex-direction: column;
  }
  
  .loading-container {
    padding: 30px 20px;
  }
  
  .loading-spinner {
    width: 50px;
    height: 50px;
  }
  
  /* 简历预览响应式优化 */
  .resume-preview {
    padding: 20px !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
  }
  
  .resume-preview h1 {
    font-size: 24px !important;
  }
  
  .resume-preview h2 {
    font-size: 20px !important;
  }
  
  .resume-preview h3 {
    font-size: 16px !important;
    padding: 10px 12px !important;
  }
  
  /* 代码块响应式优化 */
  .resume-preview pre {
    padding: 15px !important;
    font-size: 13px !important;
  }
  
  /* 表格响应式优化 */
  .resume-preview table {
    display: block !important;
    overflow-x: auto !important;
    white-space: nowrap !important;
  }
  
  /* 列表响应式优化 */
  .resume-preview ul,
  .resume-preview ol {
    margin: 10px 0 10px 15px !important;
    padding-left: 15px !important;
  }
  
  /* 个人信息响应式优化 */
  .resume-preview > p:first-child,
  .resume-preview > p:nth-child(2) {
    font-size: 16px !important;
    line-height: 2.0 !important;
  }
}

/* 平板设备优化 */
@media (min-width: 769px) and (max-width: 1024px) {
  .resume-preview {
    padding: 30px !important;
  }
  
  .preview-text {
    max-height: 600px !important;
  }
}
</style>