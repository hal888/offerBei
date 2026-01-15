import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { initAnalytics } from './utils/analytics'

// Initialize analytics
initAnalytics()

// 性能监控 - 页面加载时间
if (typeof window !== 'undefined' && window.performance) {
  // 监控页面加载完成时间
  window.addEventListener('load', () => {
    const perfData = window.performance.timing;
    const loadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log(`页面加载时间: ${loadTime}ms`);

    // 监控首屏渲染时间
    const firstPaint = perfData.responseStart - perfData.navigationStart;
    console.log(`首屏渲染时间: ${firstPaint}ms`);

    // 监控资源加载时间
    const resources = window.performance.getEntriesByType('resource');
    const resourceLoadTime = resources.reduce((total, resource) => total + resource.duration, 0);
    console.log(`资源加载总时间: ${resourceLoadTime}ms`);
  });
}

// 创建性能监控装饰器
function monitorPerformance(func, funcName) {
  return function (...args) {
    if (typeof window !== 'undefined' && window.performance && import.meta.env.DEV) {
      const start = performance.now();
      const result = func.apply(this, args);
      const end = performance.now();
      console.log(`${funcName} 执行时间: ${end - start}ms`);
      return result;
    }
    return func.apply(this, args);
  };
}

// 为Vue应用添加性能监控
const app = createApp(App)

// 在开发环境下启用组件渲染监控
if (import.meta.env.DEV) {
  app.mixin({
    beforeCreate() {
      if (this.$options.name) {
        this._componentStart = performance.now();
      }
    },
    mounted() {
      if (this.$options.name) {
        const end = performance.now();
        const duration = end - this._componentStart;
        console.log(`组件 ${this.$options.name} 渲染时间: ${duration}ms`);
      }
    }
  });
}

import i18n from './i18n'

app.use(i18n) // i18n must be registered before router for meta title translation
app.use(router)

// 监控应用挂载时间
const mountStart = performance.now();
app.mount('#app');
const mountEnd = performance.now();
console.log(`应用挂载时间: ${mountEnd - mountStart}ms`);
