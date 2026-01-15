/**
 * 智能语言检测工具
 * 优先级：用户手动选择 > 浏览器语言 > IP地理位置（兜底）
 */

const SUPPORTED_LOCALES = ['zh', 'en']
const DEFAULT_LOCALE = 'zh'
const STORAGE_KEY = 'user-locale'
const IP_LOCALE_CACHE_KEY = 'ip-locale-cache'
const IP_CACHE_DURATION = 7 * 24 * 60 * 60 * 1000 // 7天

/**
 * 1. 获取用户手动保存的语言（最高优先级）
 */
export function getUserSavedLocale() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY)
        if (saved && SUPPORTED_LOCALES.includes(saved)) {
            console.log('[Language Detection] Using user saved locale:', saved)
            return saved
        }
    } catch (e) {
        console.warn('[Language Detection] Failed to read localStorage:', e)
    }
    return null
}

/**
 * 2. 检测浏览器语言（中等优先级）
 */
export function getBrowserLocale() {
    try {
        // 获取浏览器语言
        const browserLang = navigator.language || navigator.userLanguage
        console.log('[Language Detection] Browser language:', browserLang)

        // 提取语言代码（例如 'zh-CN' -> 'zh', 'en-US' -> 'en'）
        const langCode = browserLang.split('-')[0].toLowerCase()

        // 检查是否在支持的语言列表中
        if (SUPPORTED_LOCALES.includes(langCode)) {
            console.log('[Language Detection] Using browser locale:', langCode)
            return langCode
        }

        // 如果浏览器语言不在支持列表中，返回null
        console.log('[Language Detection] Browser locale not supported:', langCode)
    } catch (e) {
        console.warn('[Language Detection] Failed to detect browser language:', e)
    }
    return null
}

/**
 * 3. 基于IP获取地理位置语言（兜底，可选）
 * 使用免费API，带缓存机制
 */
export async function getIPBasedLocale() {
    try {
        // 检查缓存
        const cached = localStorage.getItem(IP_LOCALE_CACHE_KEY)
        if (cached) {
            const { locale, timestamp } = JSON.parse(cached)
            if (Date.now() - timestamp < IP_CACHE_DURATION) {
                console.log('[Language Detection] Using cached IP locale:', locale)
                return locale
            }
        }

        // 调用IP地理位置API（使用超时保护）
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 3000) // 3秒超时

        const response = await fetch('https://ipapi.co/json/', {
            signal: controller.signal
        })
        clearTimeout(timeoutId)

        if (!response.ok) {
            throw new Error('IP API request failed')
        }

        const data = await response.json()
        const countryCode = data.country_code?.toUpperCase()

        // 根据国家代码判断语言
        let locale = DEFAULT_LOCALE
        if (countryCode === 'CN' || countryCode === 'TW' || countryCode === 'HK' || countryCode === 'MO') {
            locale = 'zh'
        } else {
            locale = 'en'
        }

        // 缓存结果
        localStorage.setItem(IP_LOCALE_CACHE_KEY, JSON.stringify({
            locale,
            timestamp: Date.now()
        }))

        console.log('[Language Detection] Using IP-based locale:', locale, '(Country:', countryCode, ')')
        return locale
    } catch (e) {
        if (e.name === 'AbortError') {
            console.warn('[Language Detection] IP detection timeout')
        } else {
            console.warn('[Language Detection] Failed to detect IP locale:', e)
        }
    }
    return null
}

/**
 * 综合判断初始语言
 * 按优先级依次尝试：用户保存 -> 浏览器语言 -> IP地理位置 -> 默认中文
 */
export async function detectInitialLocale(options = {}) {
    const { enableIPDetection = false } = options

    console.log('[Language Detection] Starting language detection...')

    // 优先级1: 用户手动保存的语言
    const userLocale = getUserSavedLocale()
    if (userLocale) {
        return userLocale
    }

    // 优先级2: 浏览器语言
    const browserLocale = getBrowserLocale()
    if (browserLocale) {
        return browserLocale
    }

    // 优先级3: IP地理位置（可选，异步）
    if (enableIPDetection) {
        const ipLocale = await getIPBasedLocale()
        if (ipLocale) {
            return ipLocale
        }
    }

    // 兜底: 使用默认语言
    console.log('[Language Detection] Using default locale:', DEFAULT_LOCALE)
    return DEFAULT_LOCALE
}

/**
 * 同步版本的语言检测（不包含IP检测）
 * 用于i18n初始化时的快速检测
 */
export function detectInitialLocaleSync() {
    console.log('[Language Detection] Starting sync language detection...')

    // 优先级1: 用户手动保存的语言
    const userLocale = getUserSavedLocale()
    if (userLocale) {
        return userLocale
    }

    // 优先级2: 浏览器语言
    const browserLocale = getBrowserLocale()
    if (browserLocale) {
        return browserLocale
    }

    // 兜底: 使用默认语言
    console.log('[Language Detection] Using default locale:', DEFAULT_LOCALE)
    return DEFAULT_LOCALE
}
