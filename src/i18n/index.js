import { createI18n } from 'vue-i18n'
import zh from '../locales/zh'
import en from '../locales/en'
import { detectInitialLocaleSync } from '../utils/languageDetector'

const i18n = createI18n({
    legacy: false, // Use Composition API mode
    locale: detectInitialLocaleSync(), // 使用智能语言检测
    fallbackLocale: 'zh',
    messages: {
        zh,
        en
    }
})

export default i18n
