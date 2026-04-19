"""
html_fetcher.py
HTML 取得（Requests / Playwright）
"""
import logging
import requests
import asyncio
import warnings
from playwright.async_api import async_playwright
from config import DEFAULT_HEADERS, REQUEST_TIMEOUT, CRAWL_TIMEOUT
from cache_manager import get_cached_html, set_cached_html

# SSL警告を抑制
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)

def fetch_html_requests(url):
    """Requests で HTML を取得"""
    try:
        response = requests.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
            verify=False
        )
        
        if response.status_code == 404:
            logger.warning(f"⚠️  HTTP 404: {url}")
            return None
        elif response.status_code != 200:
            logger.warning(f"⚠️  HTTP {response.status_code}: {url}")
            return None
        
        return response.text
    except requests.exceptions.Timeout:
        logger.warning(f"⏱️  タイムアウト: {url}")
        return None
    except requests.exceptions.ConnectionError:
        logger.warning(f"🔌 接続エラー: {url}")
        return None
    except Exception as e:
        logger.warning(f"❌ エラー: {url} | {e}")
        return None

async def fetch_html_playwright(url):
    """Playwright で HTML を取得（JavaScript レンダリング対応）"""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until='networkidle', timeout=CRAWL_TIMEOUT * 1000)
            content = await page.content()
            await browser.close()
            return content
    except Exception as e:
        logger.warning(f"🎭 Playwright エラー: {url} | {e}")
        return None

def fetch_html(url, use_playwright=False, use_cache=True):
    """HTML を取得（キャッシュ対応）"""
    # キャッシュから取得
    if use_cache:
        cached_html = get_cached_html(url, ttl=24)
        if cached_html:
            logger.debug(f"💾 キャッシュから取得: {url}")
            return cached_html
    
    # HTML を取得
    if use_playwright:
        html = asyncio.run(fetch_html_playwright(url))
    else:
        html = fetch_html_requests(url)
    
    # キャッシュに保存
    if html and use_cache:
        set_cached_html(url, html, ttl=24)
    
    return html