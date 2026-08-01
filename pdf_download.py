import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

# 目标网址
BASE_URL = "https://ebook.daehub.com/%E9%BE%99%E7%8F%A0%EF%BC%88%E5%85%A8%E5%BD%A9%E7%89%88%EF%BC%89/"

# 下载目录（保存到 ~/Downloads/书籍/龙珠全彩）
DOWNLOAD_DIR = os.path.expanduser("~/Downloads/书籍/龙珠全彩")

# CA 证书：优先用 macOS 系统证书，避免 conda 环境 certifi 证书链失效导致的 SSL 错误
CA_BUNDLE = "/etc/ssl/cert.pem" if os.path.exists("/etc/ssl/cert.pem") else True

# 并行下载线程数（同时下载的卷数）
MAX_WORKERS = 5

# 多线程安全的打印锁
_print_lock = threading.Lock()


def plog(msg):
    """多线程安全的打印"""
    with _print_lock:
        print(msg, flush=True)

def download_pdf(file_url, file_name, max_retries=5):
    """下载单个PDF文件到指定目录（带自动重试，适合不稳定的网络环境）"""
    # 确保下载目录存在
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    final_path = os.path.join(DOWNLOAD_DIR, file_name)

    # 如果文件已存在（且完整），跳过下载
    if os.path.exists(final_path):
        plog(f"⏭️  已跳过: {file_name} (文件已存在)")
        return True

    # 先下载到 .part 临时文件，成功后再改名，避免失败留下残缺文件
    part_path = final_path + ".part"

    for attempt in range(1, max_retries + 1):
        try:
            plog(f"⬇️  正在下载: {file_name} (第 {attempt}/{max_retries} 次尝试) ...")
            response = requests.get(
                file_url, stream=True, timeout=(10, 60), verify=CA_BUNDLE
            )
            response.raise_for_status()

            # 获取文件大小（用于显示进度）
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            last_report = -1

            with open(part_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        # 每跨过 10% 打一行进度（多线程下用独立行，避免 \r 互相覆盖）
                        if total_size > 0:
                            percent = int(100 * downloaded / total_size)
                            if percent // 10 > last_report:
                                last_report = percent // 10
                                plog(f"  [{file_name}] {percent}%")

            # 完整性校验：有 content-length 时检查大小是否一致
            if total_size > 0 and downloaded != total_size:
                raise IOError(f"文件不完整: 期望 {total_size} 字节，实际 {downloaded} 字节")

            os.replace(part_path, final_path)
            plog(f"✅ 下载完成: {file_name}")
            return True

        except (requests.exceptions.SSLError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError,
                IOError) as e:
            plog(f"⚠️  第 {attempt} 次尝试失败: {str(e)[:120]}")
            # 清理残缺的临时文件
            if os.path.exists(part_path):
                os.remove(part_path)
            if attempt < max_retries:
                wait = 2 ** (attempt - 1)  # 1, 2, 4, 8 秒退避
                plog(f"    等待 {wait} 秒后重试...")
                time.sleep(wait)
            else:
                plog(f"❌ 下载 {file_name} 失败（重试 {max_retries} 次后放弃）")
                return False

        except Exception as e:
            plog(f"❌ 下载 {file_name} 时出错: {e}")
            return False

    return False


def download_batch(pdf_list, workers=MAX_WORKERS):
    """并行批量下载（默认 5 线程），已存在的自动跳过，返回失败的卷名列表"""
    if not pdf_list:
        return []

    failed = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(download_pdf, url, name): name
                   for name, url in pdf_list}
        for fut in as_completed(futures):
            name = futures[fut]
            try:
                if not fut.result():
                    failed.append(name)
            except Exception as e:
                plog(f"❌ 下载 {name} 时出错: {e}")
                failed.append(name)
    return failed


def download_missing(pdf_list):
    """只补下载缺失的卷，返回失败的卷名列表"""
    missing = [(n, u) for n, u in pdf_list
               if not os.path.exists(os.path.join(DOWNLOAD_DIR, n))]
    if not missing:
        plog("✅ 没有缺失的文件，全部卷已下载完成！")
        return []
    plog(f"📥 发现 {len(missing)} 卷缺失，开始补下载...\n")
    return download_batch(missing)


def print_summary(failed):
    """打印下载结果汇总"""
    print("\n" + "=" * 50)
    if failed:
        print(f"⚠️  有 {len(failed)} 卷下载失败，可重跑脚本选择补下载：")
        for name in failed:
            print(f"  - {name}")
    else:
        print("🎉 所有文件下载完成！")


def get_pdf_links():
    """从目录页获取所有PDF文件的名称和完整下载链接"""
    try:
        plog("📋 正在获取文件列表...")
        response = requests.get(BASE_URL, verify=CA_BUNDLE)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_links = []
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.pdf'):
                full_url = BASE_URL + href if not href.startswith('http') else href
                file_name = link.get_text(strip=True) or href.split('/')[-1]
                pdf_links.append((file_name, full_url))
        
        return pdf_links
    except Exception as e:
        plog(f"❌ 获取文件列表失败: {e}")
        return []

if __name__ == "__main__":
    print("=" * 50)
    print("🐉 龙珠（全彩版）批量下载工具")
    print("=" * 50)
    
    pdf_list = get_pdf_links()
    
    if not pdf_list:
        print("❌ 未找到任何PDF文件，请检查网址是否有效。")
    else:
        print(f"📚 共找到 {len(pdf_list)} 卷漫画\n")
        for idx, (name, url) in enumerate(pdf_list, 1):
            print(f"  [{idx:2d}] {name}")
        print("\n" + "=" * 50)
        
        # 统计已下载和缺失
        done = sum(1 for n, _ in pdf_list
                   if os.path.exists(os.path.join(DOWNLOAD_DIR, n)))
        missing = len(pdf_list) - done
        print(f"📊 已下载: {done} 卷, 缺失: {missing} 卷\n")

        # 选择下载方式
        print("请选择下载方式:")
        print("  [1] 下载全部（已存在的自动跳过）")
        print("  [2] 只补下载缺失的")
        choice = input("请输入序号 (1/2)，直接回车取消: ").strip()

        if choice == '1':
            print("\n🚀 开始下载全部...\n")
            failed = download_batch(pdf_list)
            print_summary(failed)
        elif choice == '2':
            print()
            failed = download_missing(pdf_list)
            print_summary(failed)
        else:
            print("已取消下载。")
