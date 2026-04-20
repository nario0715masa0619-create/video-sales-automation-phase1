import os
import json
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

# キャッシング設定
CACHE_DIR = Path('cache/website_scrape')
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_cache_file(website_url):
    """キャッシュファイルパスを取得"""
    domain = urlparse(website_url).netloc
    return CACHE_DIR / f'{domain}.json'

def load_from_cache(website_url):
    """キャッシュからメール情報を読み込む"""
    cache_file = get_cache_file(website_url)
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return tuple(data.get('result', [None, None, None]))
        except:
            return None, None, None
    return None, None, None

def save_to_cache(website_url, email, contact_form_url):
    """メール情報をキャッシュに保存"""
    cache_file = get_cache_file(website_url)
    data = {
        'website': website_url,
        'result': [website_url, email, contact_form_url],
        'cached_at': datetime.now().isoformat()
    }
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pass

def show_cache_stats():
    """キャッシュの統計情報を表示"""
    cache_files = list(CACHE_DIR.glob('*.json'))
    return len(cache_files)
