import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import logging
from datetime import datetime, timedelta
from typing import List, Optional

# ===================== 配置项（请根据你的网站修改） =====================
# 百度搜索资源平台获取的token（必填）
BAIDU_TOKEN = "caPQYWw65LMAbHn9"
# 你的网站域名（例如：https://www.xxx.com）
SITE_DOMAIN = "https://offerbei.ailongdev.com"
# 生成sitemap的文件保存路径（建议放在网站根目录）
SITEMAP_SAVE_PATH = "./sitemap.xml"
# URL的更新频率（可选值：always, hourly, daily, weekly, monthly, yearly, never）
URL_CHANGE_FREQ = "daily"
# URL的优先级（0.0-1.0，首页建议1.0，栏目页0.8，内容页0.6）
URL_PRIORITY_MAP = {
    "index": 1.0,       # 首页
    "category": 0.8,    # 栏目页
    "article": 0.6      # 内容页
    
}
# 日志保存路径
LOG_FILE = "../baidu_push.log"

# ===================== 日志配置 =====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)
logger = logging.getLogger(__name__)

# ===================== Sitemap生成功能 =====================
def generate_sitemap(urls: List[dict], save_path: str = SITEMAP_SAVE_PATH) -> bool:
    """
    生成符合百度规范的XML网站地图
    :param urls: URL列表，格式示例：
        [
            {"loc": "https://www.xxx.com", "type": "index", "lastmod": "2026-01-12"},
            {"loc": "https://www.xxx.com/category", "type": "category", "lastmod": "2026-01-12"},
            {"loc": "https://www.xxx.com/article/1", "type": "article", "lastmod": "2026-01-12"}
        ]
    :param save_path: sitemap保存路径
    :return: 是否生成成功
    """
    try:
        # 创建XML根节点
        urlset = ET.Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        
        for url_info in urls:
            # 校验必要字段
            if not url_info.get("loc"):
                logger.warning(f"URL缺少loc字段，跳过：{url_info}")
                continue
            
            # 创建URL节点
            url = ET.SubElement(urlset, "url")
            
            # 核心字段：页面地址（必填）
            loc = ET.SubElement(url, "loc")
            loc.text = url_info["loc"]
            
            # 可选字段：最后更新时间（建议填写）
            if url_info.get("lastmod"):
                lastmod = ET.SubElement(url, "lastmod")
                lastmod.text = url_info["lastmod"]
            else:
                # 默认为当前日期
                lastmod = ET.SubElement(url, "lastmod")
                lastmod.text = datetime.now().strftime("%Y-%m-%d")
            
            # 可选字段：更新频率
            changefreq = ET.SubElement(url, "changefreq")
            changefreq.text = URL_CHANGE_FREQ
            
            # 可选字段：优先级
            priority = ET.SubElement(url, "priority")
            priority.text = str(URL_PRIORITY_MAP.get(url_info.get("type"), 0.6))
        
        # 美化XML格式（便于阅读和百度识别）
        rough_xml = ET.tostring(urlset, encoding="utf-8")
        parsed_xml = minidom.parseString(rough_xml)
        pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8")
        
        # 写入文件（解决minidom自动添加的多余xml声明问题）
        with open(save_path, "wb") as f:
            # 去掉多余的空行和重复的xml声明
            lines = pretty_xml.decode("utf-8").split("\n")
            clean_lines = [line for line in lines if line.strip() and not line.strip().startswith("<?xml")]
            newline = "\n"
            f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n{newline.join(clean_lines)}'.encode("utf-8"))
        
        logger.info(f"Sitemap生成成功，保存路径：{save_path}")
        return True
    
    except Exception as e:
        logger.error(f"生成Sitemap失败：{str(e)}")
        return False

# ===================== 百度API主动推送功能 =====================
def baidu_api_push(urls: List[str]) -> Optional[dict]:
    """
    调用百度普通收录API推送URL
    :param urls: 要推送的URL列表（例如：["https://www.xxx.com", "https://www.xxx.com/article/1"]）
    :return: 百度返回的响应结果（字典），失败返回None
    """
    if not BAIDU_TOKEN or not SITE_DOMAIN:
        logger.error("请先配置BAIDU_TOKEN和SITE_DOMAIN")
        return None
    
    if not urls:
        logger.warning("推送的URL列表为空")
        return None
    
    # 百度API接口
    api_url = f"http://data.zz.baidu.com/urls?site={SITE_DOMAIN}&token={BAIDU_TOKEN}"
    
    # 请求头（必须指定，否则可能推送失败）
    headers = {
        "Content-Type": "text/plain",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BaiduPushBot/1.0"
    }
    
    try:
        # 推送URL（多个URL用换行分隔）
        response = requests.post(
            api_url,
            data="\n".join(urls).encode("utf-8"),
            headers=headers,
            timeout=10  # 设置超时时间，避免卡壳
        )
        
        # 解析响应结果
        result = response.json()
        if result.get("success") > 0:
            logger.info(f"成功推送{result['success']}个URL，剩余配额：{result['remain']}")
        else:
            logger.warning(f"推送失败，响应结果：{result}")
        
        return result
    
    except requests.exceptions.Timeout:
        logger.error("百度API推送超时，请检查网络或稍后重试")
    except requests.exceptions.ConnectionError:
        logger.error("无法连接到百度API，请检查网络")
    except Exception as e:
        logger.error(f"API推送异常：{str(e)}")
    
    return None

# ===================== 示例：批量处理 =====================
def main():
    """
    主函数：生成sitemap + 推送URL
    你可以根据自己的网站逻辑，替换成从数据库/文件读取URL的逻辑
    """
    # 1. 准备你的网站URL列表（示例，需替换为真实URL）
    website_urls = [
        {"loc": f"{SITE_DOMAIN}", "type": "index", "lastmod": datetime.now().strftime("%Y-%m-%d")},
        {"loc": f"{SITE_DOMAIN}/manual", "type": "manual", "lastmod": datetime.now().strftime("%Y-%m-%d")},
        {"loc": f"{SITE_DOMAIN}/faq", "type": "faq", "lastmod": datetime.now().strftime("%Y-%m-%d")}
    ]
    
    # 2. 生成sitemap.xml
    generate_sitemap(website_urls)
    
    # 3. 提取URL列表用于API推送
    push_urls = [url["loc"] for url in website_urls]
    
    # 4. 调用百度API推送
    baidu_api_push(push_urls)

if __name__ == "__main__":
    main()