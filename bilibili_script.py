import requests
import json
import time
import re
import argparse
import sys
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

'''
B站评论抓取脚本，输出格式为 JSON / CSV / XLSX，优先尝试 JSON。
使用方法：
    python bilibili_script.py "https://www.bilibili.com/video/BVxxxx" 
'''

def bv_to_aid(bvid: str) -> int:
    """获取视频的 aid/oid"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers).json()
    if resp["code"] == 0:
        return resp["data"]["aid"]
    raise ValueError(f"获取视频信息失败: {resp['message']}")

def fetch_comments(bvid: str, max_pages: int = 5, session: requests.Session | None = None, timeout: float = 10.0, verify: bool = True):
    """抓取主评论"""
    aid = bv_to_aid(bvid)
    base_url = "https://api.bilibili.com/x/v2/reply/main"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/{bvid}"
    }

    if session is None:
        session = requests.Session()

    next_cursor = 0
    comments = []

    for page in range(1, max_pages + 1):
        params = {
            "type": 1,         # 1 代表视频稿件
            "oid": aid,
            "mode": 3,         # 3 代表按热度排序，2 代表按时间排序
            "next": next_cursor
        }

        try:
            resp_obj = session.get(base_url, headers=headers, params=params, timeout=timeout, verify=verify)
            resp_obj.raise_for_status()
            resp = resp_obj.json()
        except requests.exceptions.SSLError as e:
            print(f"SSL 错误: {e}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            break

        if resp.get("code") != 0:
            print(f"请求失败: {resp.get('message')}")
            break

        data = resp.get("data", {})
        replies = data.get("replies") or []

        if not replies:
            print("没有更多评论了。")
            break

        for reply in replies:
            user = reply["member"]["uname"]
            content = reply["content"]["message"]
            likes = reply["like"]
            comments.append({"user": user, "content": content, "likes": likes})
            print(f"[{user}] (点赞 {likes}): {content}\n")

        cursor_data = data.get("cursor", {})
        if cursor_data.get("is_end"):
            break
        next_cursor = cursor_data.get("next", 0)
        time.sleep(1)  # 避免请求过快触发风控

    return comments

if __name__ == "__main__":
    def extract_bvid(s: str) -> str:
        """从 URL 或直接给定的字符串中提取 BV 号（只支持 BV 形式）。"""
        m = re.search(r'(BV[0-9A-Za-z]+)', s)
        if m:
            return m.group(1)
        raise ValueError("无法从输入中提取 BV ID，请提供包含 BVxxxx 的 URL 或直接提供 BV 号。")

    def save_comments(comments, path: str):
        """根据文件扩展名保存为 JSON / CSV / XLSX，优先尝试 JSON。"""
        if not comments:
            print("没有评论需要保存。")
            return

        lower = path.lower()
        if lower.endswith('.json'):
            # 使用 utf-8 编码并保持中文可读
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(comments, f, ensure_ascii=False, indent=2)
                print(f"已保存 {len(comments)} 条评论到 {path}")
                return
            except Exception as e:
                print(f"保存 JSON 时出错: {e}")
                raise

        # 对于 xlsx/csv，使用 pandas
        df = pd.DataFrame(comments)
        if lower.endswith('.csv'):
            df.to_csv(path, index=False)
            print(f"已保存 {len(comments)} 条评论到 {path}")
            return

        if lower.endswith('.xlsx'):
            try:
                df.to_excel(path, index=False, engine="openpyxl")
                print(f"已保存 {len(comments)} 条评论到 {path}")
                return
            except ModuleNotFoundError:
                csv_path = path[:-5] + '.csv'
                df.to_csv(csv_path, index=False)
                print(f"未检测到 openpyxl，已改为保存为 CSV: {csv_path}")
                print("若需导出为 Excel，请运行: pip install openpyxl && 再次运行脚本。")
                return
            except Exception as e:
                print(f"保存 XLSX 时出错: {e}")
                raise

        # 默认回退为 JSON
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(comments, f, ensure_ascii=False, indent=2)
            print(f"已保存 {len(comments)} 条评论到 {path} (作为 JSON)")
        except Exception as e:
            print(f"保存文件时发生错误: {e}")
            raise

    parser = argparse.ArgumentParser(description="抓取哔哩哔哩视频评论并保存为 Excel。可传入完整 URL 或 BV 号。")
    parser.add_argument("input", help="视频 URL 或 BV 标识，例如 https://www.bilibili.com/video/BVxxxx 或 BVxxxx")
    parser.add_argument("-p", "--pages", type=int, default=20, help="抓取的页数，默认 20")
    parser.add_argument("-o", "--out", default="bilibili_comments.json", help="输出文件路径（.json/.csv/.xlsx），默认 bilibili_comments.json")
    parser.add_argument("--insecure", action="store_true", help="跳过 SSL 证书验证（不安全，仅用于排查）")
    parser.add_argument("--timeout", type=float, default=10.0, help="单次请求超时（秒），默认 10")
    parser.add_argument("--retries", type=int, default=5, help="网络层重试次数，默认 5")

    args = parser.parse_args()
    try:
        bvid = extract_bvid(args.input)
    except ValueError as e:
        print(e)
        sys.exit(1)

    def make_session(retries: int = 5, backoff_factor: float = 0.5):
        s = requests.Session()
        retry = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
        return s

    session = make_session(retries=args.retries)
    try:
        comments = fetch_comments(bvid, max_pages=args.pages, session=session, timeout=args.timeout, verify=not args.insecure)
    except requests.exceptions.SSLError:
        print("检测到 SSL 错误。可尝试加上 --insecure 跳过证书验证（不安全），或更新系统证书/Python/OpenSSL。")
        sys.exit(1)

    save_comments(comments, args.out)