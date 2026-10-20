import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# 基础配置
BASE_URL = "https://meirentu.art/pic/207993498722.html"  # 起始页 URL
SAVE_DIR = "downloaded_images"

# 伪造浏览器请求头（Referer 用于防盗链，图片在 p11.mmdb.cc 图床）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    'Referer': 'https://meirentu.art/'
}

# 图片域名白名单：只下载正文图床的图片，跳过 logo、头像、推荐缩略图等
IMG_HOST_WHITELIST = {"p11.mmdb.cc"}

# 安全上限：防止死循环（正常情况下空页检测会提前停止）
MAX_PAGES = 50
# 每页最大重试次数与退避间隔（秒）
RETRIES = 3
BACKOFF = 3

# 全局 Session：复用 TCP 连接，减少 SSL 握手次数，降低触发断连的概率
session = requests.Session()
session.headers.update(HEADERS)


def get_soup(url):
    """获取页面并解析为 BeautifulSoup 对象"""
    response = session.get(url, timeout=15)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, 'html.parser')


def fetch_with_retry(url):
    """带重试的页面获取；全部失败返回 None（由调用方决定跳过）"""
    for attempt in range(1, RETRIES + 1):
        try:
            return get_soup(url)
        except Exception as e:
            print(f"  ⚠️  第 {attempt}/{RETRIES} 次请求失败: {type(e).__name__}: {e}")
            if attempt < RETRIES:
                time.sleep(BACKOFF * attempt)  # 3s、6s 退避
    return None


def build_page_url(page_no):
    """按站点分页规律生成 URL：第 1 页无后缀，第 n 页为 {id}-{n}.html"""
    if page_no == 1:
        return BASE_URL
    return BASE_URL.replace('.html', f'-{page_no}.html')


def parse_pagination(soup):
    """从页面底部分页导航（1 2 3 ... 28）提取页码链接"""
    page_nums = {1}
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        # 匹配形如 ...207993498722-3.html 的分页链接
        m = re.search(r'-(\d+)\.html$', href)
        if m:
            full = urljoin(BASE_URL, href)
            if full.startswith(BASE_URL.split('.html')[0]):
                page_nums.add(int(m.group(1)))
    return sorted(page_nums)


def get_total_pages(soup):
    """确定总页数：分页导航页码 + 标题里的 P 数 + 末页按钮，三处交叉取最大值"""
    candidates = []

    # 1) 分页导航里的最大页码（可能只显示前 10 页）
    page_nums = parse_pagination(soup)
    if page_nums:
        candidates.append(max(page_nums))

    # 2) 标题里的 "84P" → 每页 3 张 → ceil(84/3) = 28 页
    title = soup.title.string if soup.title else ""
    m = re.search(r'(\d+)\s*P', title)
    if m:
        candidates.append(-(-int(m.group(1)) // 3))  # 向上取整

    # 3) "末页/尾页/»" 按钮直接指向的页码
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        if text in ("末页", "尾页", "最后一页", ">|", "»", "»"):
            m = re.search(r'-(\d+)\.html$', a['href'])
            if m:
                candidates.append(int(m.group(1)))

    total = max(candidates) if candidates else MAX_PAGES
    return min(total, MAX_PAGES)


def get_img_urls(soup, seen):
    """解析页面正文图片，返回去重后的新图片 URL 列表"""
    image_urls = []
    for img in soup.find_all('img'):
        img_url = img.get('data-src') or img.get('src') or img.get('data-original')
        if not img_url:
            continue
        full_url = urljoin(BASE_URL, img_url).split('?')[0]
        # 只收白名单图床 + jpg/jpeg 后缀 + 去重
        if urlparse(full_url).netloc not in IMG_HOST_WHITELIST:
            continue
        if not full_url.lower().endswith(('.jpg', '.jpeg')):
            continue
        if full_url in seen:
            continue
        seen.add(full_url)
        image_urls.append(full_url)
    return image_urls


def download_image(img_url, save_dir):
    """下载单张图片"""
    filename = img_url.split('/')[-1]  # 形如 00225127.jpg
    save_path = os.path.join(save_dir, filename)
    if os.path.exists(save_path):
        print(f"⏭️  已存在，跳过: {filename}")
        return False
    try:
        response = session.get(img_url, timeout=15)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ 下载成功: {filename}")
        time.sleep(0.5)  # 礼貌性延时
        return True
    except Exception as e:
        print(f"❌ 下载失败: {img_url} - 原因: {e}")
        return False


def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    print(f"⏳ 访问首页: {BASE_URL}")
    soup = get_soup(BASE_URL)

    # 先确定总页数（分页导航 + 标题 84P + 末页按钮交叉确认）
    total_pages = get_total_pages(soup)
    print(f"📄 确认共 {total_pages} 页，开始依次抓取，失败页自动跳过并在最后重试")

    seen = set()            # 全局去重
    count = 0
    failed_pages = []       # 记录失败的页码，最后统一补抓

    for page_no in range(1, total_pages + 1):
        page_url = build_page_url(page_no)
        print(f"\n⏳ 正在处理第 {page_no}/{total_pages} 页: {page_url}")

        soup = fetch_with_retry(page_url)
        if soup is None:
            print(f"❗ 第 {page_no} 页多次请求失败，先跳过，稍后统一重试。")
            failed_pages.append(page_no)
            time.sleep(2)
            continue

        img_urls = get_img_urls(soup, seen)
        if not img_urls:
            print(f"❗ 第 {page_no} 页无新图片（可能已到末尾或该页为空）")
        else:
            for img_url in img_urls:
                if download_image(img_url, SAVE_DIR):
                    count += 1

        time.sleep(1.5)  # 翻页延时

    # 最后对失败页面再做一轮补抓
    if failed_pages:
        print(f"\n🔄 对 {len(failed_pages)} 个失败页面进行补抓: {failed_pages}")
        still_failed = []
        for page_no in failed_pages:
            page_url = build_page_url(page_no)
            print(f"\n⏳ 补抓第 {page_no} 页: {page_url}")
            soup = fetch_with_retry(page_url)
            if soup is None:
                print(f"❗ 第 {page_no} 页补抓仍失败，放弃。")
                still_failed.append(page_no)
                continue
            img_urls = get_img_urls(soup, seen)
            for img_url in img_urls:
                if download_image(img_url, SAVE_DIR):
                    count += 1
            time.sleep(1.5)
        if still_failed:
            print(f"⚠️  以下页面最终仍失败，可稍后重跑脚本（已下载的图片会自动跳过）: {still_failed}")

    print(f"\n🎉 爬取完成，共下载 {count} 张新图片，保存至 ./{SAVE_DIR}/")


if __name__ == "__main__":
    main()