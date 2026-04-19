"""
website_crawler.py
ドメイン内のページをクロール
"""
import logging
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from html_fetcher import fetch_html

logger = logging.getLogger(__name__)

# クロール対象外のファイルタイプ
SKIP_EXTENSIONS = {
    '.pdf', '.zip', '.exe', '.dmg', '.tar', '.gz',
    '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',
    '.mp3', '.mp4', '.avi', '.mov', '.wav',
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.csv', '.json', '.xml', '.yml', '.yaml'
}

def should_skip_url(url):
    """URL をスキップすべきかチェック"""
    # ファイルタイプをチェック
    for ext in SKIP_EXTENSIONS:
        if url.lower().endswith(ext):
            return True
    
    # クエリパラメータが多い URL をスキップ
    if url.count('?') > 1:
        return True
    
    return False

def crawl_domain(start_url, max_pages=20):
    """ドメイン内をクロール"""
    visited = set()
    to_visit = [start_url]
    domain = urlparse(start_url).netloc
    html_list = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        
        if url in visited:
            continue
        
        # スキップ判定
        if should_skip_url(url):
            logger.debug(f"⏭️  スキップ: {url}")
            visited.add(url)
            continue
        
        visited.add(url)
        
        # HTML 取得
        html = fetch_html(url)
        if not html:
            logger.debug(f"❌ HTML 取得失敗: {url}")
            continue
        
        logger.info(f"   🔗 クロール: {url}")
        html_list.append(html)
        
        # リンク抽出
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a', href=True):
                link = urljoin(url, a['href'])
                
                # 同一ドメインかチェック
                if urlparse(link).netloc != domain:
                    continue
                
                # フラグメント削除
                link = link.split('#')[0]
                
                # 重複チェック
                if link not in visited and link not in to_visit:
                    to_visit.append(link)
        except Exception as e:
            logger.debug(f"リンク抽出エラー: {e}")
    
    return html_list