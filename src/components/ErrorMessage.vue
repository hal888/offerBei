<template>
  <div v-if="show" class="error-overlay">
    <div class="error-modal" @click.stop>
      <div class="error-content">
        <p class="error-message">{{ message }}</p>
      </div>
      <div class="error-footer">
        <button class="error-button" @click="close">{{ t('alerts.confirm') }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  message: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: '' // Default handled in template or logic, but here we can just leave empty and header logic (if any)
  }
})

// Emits
const emit = defineEmits(['close'])

// 移除调试代码，避免不必要的日志输出

// 关闭错误提示
const close = () => {
  emit('close')
}
</script>

<style scoped>
.error-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.error-modal {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 400px;
  overflow: hidden;
  animation: slideIn 0.3s ease;
}

/* 简化样式，移除header和close按钮相关样式 */

.error-content {
  padding: 24px 20px;
}

.error-content .error-message {
  font-size: 16px;
  color: #333;
  margin: 0;
  text-align: center;
  line-height: 1.5;
}

.error-footer {
  padding: 0 20px 20px;
  display: flex;
  justify-content: center;
}

.error-button {
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
}

.error-button:hover {
  background-color: #5a6fd8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>