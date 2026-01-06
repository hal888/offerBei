import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
import time

# 配置参数
BASE_URL = "http://localhost:5173"  # 本地开发环境URL
EXCLUDE_PATHS = ["/admin", "/login", "/register"]  # 排除的页面路径
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

def get_all_links(url, visited=None):
    """递归抓取网站所有链接"""
    if visited is None:
        visited = set()
    
    if url in visited:
        return visited
    
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        if response.headers.get("Content-Type", "").startswith("text/html"):
            visited.add(url)
            soup = BeautifulSoup(response.text, "lxml")
            
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                # 处理相对链接
                if href.startswith("/") and not href.startswith("//"):
                    href = BASE_URL + href
                elif href.startswith(BASE_URL):
                    pass
                else:
                    continue  # 跳过外部链接
                
                # 排除指定路径
                if any(exclude in href for exclude in EXCLUDE_PATHS):
                    continue
                
                if href not in visited:
                    visited = get_all_links(href, visited)
                    
    except Exception as e:
        print(f"抓取链接失败 {url}: {e}")
    
    time.sleep(0.5)  # 避免频繁请求被封
    return visited

def generate_sitemap(links, output_file="sitemap.xml"):
    """生成XML站点地图"""
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for link in sorted(links):
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = link
        
        lastmod = ET.SubElement(url, "lastmod")
        lastmod.text = time.strftime("%Y-%m-%d")  # 简化处理，实际可根据文件修改时间调整
        
        changefreq = ET.SubElement(url, "changefreq")
        changefreq.text = "weekly" if "/blog" in link else "monthly"
        
        priority = ET.SubElement(url, "priority")
        priority.text = "1.0" if link == BASE_URL else "0.8" if "/blog" in link else "0.5"
    
    # 美化XML格式
    rough_string = ET.tostring(urlset, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # 写入文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    
    print(f"站点地图已生成：{output_file}")
    print(f"共包含 {len(links)} 个页面")

if __name__ == "__main__":
    print("开始抓取网站链接...")
    all_links = get_all_links(BASE_URL)
    print(f"共抓取到 {len(all_links)} 个有效链接")
    
    print("开始生成站点地图...")
    generate_sitemap(all_links)