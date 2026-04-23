"""
website_scraper_v2.py
メインスクリプト（モジュール化版）
"""

import logging
import sys
from config import LOG_FILE
from cache_manager import init_cache, get_cache_stats, clear_cache
from crm_manager import read_website_urls_from_crm
from phone_extractor import extract_phone
from website_crawler import crawl_domain
from company_info_extractor import extract_company_name

logger = logging.getLogger(__name__)

def setup_logging():
    """ログ設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def should_skip_url(url):
    """URL をスキップすべきか判定"""
    from config import SKIP_URL_PATTERNS
    import re
    for pattern in SKIP_URL_PATTERNS:
        if re.search(pattern, url):
            return True
    return False

def scrape_website(url_data):
    """単一の Website をスクレイピング"""
    row_index, website_url, email, crm_company_name = url_data
    
    logger.info(f"Row {row_index} → {website_url}")
    
    # スキップ判定
    if should_skip_url(website_url):
        logger.info(f"   ⏭️  スキップ（短縮URL等）")
        return {
            'company_name': crm_company_name,
            'phone_number': None,
            'status': 'skipped',
            'url': website_url
        }
    
    # クロール実行
    html_list = crawl_domain(website_url)
    
    if not html_list:
        logger.info(f"   ❌ HTML 取得失敗")
        return {
            'company_name': crm_company_name,
            'phone_number': None,
            'status': 'invalid',
            'url': website_url
        }
    
    # 企業名抽出
    company_name = extract_company_name(html_list[0], website_url, crm_company_name)
    
    # 電話番号抽出（複数ページから試す）
    phone_number = None
    for html in html_list:
        phone = extract_phone(html)
        if phone:
            phone_number = phone
            break
    
    # Status 判定
    status = 'ready_to_contact' if phone_number else 'invalid'
    
    return {
        'company_name': company_name,
        'phone_number': phone_number,
        'status': status,
        'url': website_url
    }

def run_batch_scraping(limit=None):
    """バッチ処理でスクレイピング実行"""
    logger.info("=" * 80)
    logger.info("🚀 batch scraping 開始")
    logger.info("=" * 80)
    
    # CRM から URL リストを読み込み
    url_list = read_website_urls_from_crm(limit)
    logger.info(f"📋 CRM から {len(url_list)} 件の URL を読み込みました")
    
    # 処理開始
    success_count = 0
    for idx, url_data in enumerate(url_list, 1):
        result = scrape_website(url_data)
        
        # Phase 5 に保存
        # append_to_gsheet_phase5(
            result['company_name'],
            result['phone_number'],
            result['status'],
            result['url']
        # )
        
        if result['status'] == 'ready_to_contact':
            success_count += 1
        
        # 進捗表示
        logger.info(f"Progress: {idx}/{len(url_list)}")
    
    # 統計情報
    logger.info("=" * 80)
    logger.info(f"Completed: {len(url_list)} items, {success_count} with phone numbers")
    logger.info("=" * 80)
    
    # キャッシュ統計
    cache_stats = get_cache_stats()
    logger.info(f"💾 キャッシュ統計: {cache_stats[0]} URLs, {cache_stats[1]} MB")

def main():
    """メイン処理"""
    setup_logging()
    
    # キャッシュを初期化
    init_cache()
    
    # コマンドライン引数を解析
    limit = None
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=')[1])
            logger.info(f"📋 オプション: limit={limit}")
        elif arg == '--clear-cache':
            logger.info("🧹 キャッシュをクリアします")
            clear_cache()
            return
    
    logger.info("=" * 80)
    
    # バッチ処理実行
    run_batch_scraping(limit)

if __name__ == '__main__':
    main()