"""
website_scraper.py（修正版 v3 - 認証修正版）
CRM Google Sheet から Website URL を読み込み、
各サイトをスクレイピングして会社名・電話番号を抽出し、
Phase 5 Google Sheet に保存する
"""

import logging
import re
import requests
import json
import os
import sys
import time
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials
import gspread

# ===== 環境設定 =====
load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SPREADSHEET_ID_PHASE5 = os.getenv('SPREADSHEET_ID_PHASE5')
SHEET_NAME_CRM = os.getenv('SHEET_NAME_CRM', 'Leads')
SHEET_NAME_PHASE5 = os.getenv('SHEET_NAME_PHASE5', 'leads')

# ===== ロギング設定 =====
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('website_scraper.log', encoding='utf-8')
        ]
    )
    # Requests ライブラリの警告を抑制
    requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)

# ===== スキップ対象 URL パターン =====
SKIP_URL_PATTERNS = [
    r'lin\.ee',
    r'forms\.google\.com',
    r'forms\.office\.com',
    r'typeform\.com',
]

# ===== 優先パス =====
PRIORITY_PATHS = [
    '/contact', '/inquiry', '/company', '/about', '/privacy',
    '/お問い合わせ', '/お問合せ', '/会社概要', '/about-us',
]

# ===== 電話番号パターン =====
PHONE_PATTERNS = [
    r'0\d{1,4}[-\s]?\d{1,4}[-\s]?\d{4}',
    r'\+81[-\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d{4}',
]

# ===== Google Sheets クライアント =====
def get_gsheet_client():
    """Google Sheets API クライアントを初期化"""
    try:
        credentials = Credentials.from_service_account_file(
            'credentials/service_account.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        return gspread.authorize(credentials)
    except Exception as e:
        logger.error(f"❌ Google Sheets 認証エラー: {e}")
        return None

# ===== CRM から URL リスト取得 =====
def read_website_urls_from_crm(limit=None):
    """CRM Sheet から Website URL を読み込み"""
    try:
        client = get_gsheet_client()
        if not client:
            logger.error("Google Sheets クライアント初期化失敗")
            return []
        
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(SHEET_NAME_CRM)
        rows = worksheet.get_all_values()
        
        results = []
        for idx, row in enumerate(rows[1:], start=2):
            if len(row) < 5:
                continue
            
            website_url = row[4].strip() if len(row) > 4 else ''
            company_name = row[0].strip() if len(row) > 0 else ''
            email = row[1].strip() if len(row) > 1 else ''
            
            if website_url and website_url.startswith(('http://', 'https://')):
                logger.info(f"📌 Row {idx}: {website_url}")
                results.append({
                    'row_index': idx,
                    'website_url': website_url,
                    'email': email,
                    'company_name': company_name
                })
        
        logger.info(f"✅ CRM から {len(results)} 件の URL を読み込みました")
        
        if limit:
            results = results[:limit]
            logger.info(f"📊 --limit {limit} で {len(results)} 件に制限しました")
        
        return results
    except Exception as e:
        logger.error(f"❌ CRM 読み込みエラー: {e}")
        return []

# ===== Phase 5 Sheet へ保存 =====
def append_to_gsheet_phase5(company_name, phone_number, status, website_url):
    """Phase 5 Sheet にデータを追加"""
    try:
        client = get_gsheet_client()
        if not client:
            logger.error("Google Sheets クライアント初期化失敗")
            return False
        
        spreadsheet = client.open_by_key(SPREADSHEET_ID_PHASE5)
        worksheet = spreadsheet.worksheet(SHEET_NAME_PHASE5)
        row_data = [company_name, phone_number, status, website_url, time.strftime('%Y-%m-%d %H:%M:%S')]
        worksheet.append_row(row_data)
        logger.info(f"💾 Phase 5 に保存: {company_name} | {phone_number} | {status}")
        return True
    except Exception as e:
        logger.error(f"❌ Phase 5 保存エラー: {e}")
        return False

# ===== ユーティリティ関数 =====
def is_valid_phone(phone_str):
    """電話番号形式の検証（10 桁以上）"""
    if not phone_str:
        return False
    cleaned = re.sub(r'[\s\-\(\)]', '', phone_str)
    if not re.match(r'^\d+$', cleaned):
        return False
    return len(cleaned) >= 10

def should_skip_url(url):
    """スキップ対象 URL かチェック"""
    for pattern in SKIP_URL_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            logger.info(f"⏭️  スキップ: {url} (パターン: {pattern})")
            return True
    return False

# ===== HTML 取得 =====
def fetch_html(url, timeout=10):
    """URL から HTML を取得"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, verify=False)
        
        if response.status_code == 404:
            logger.warning(f"⚠️  404 Not Found: {url}")
            return None
        
        if response.status_code != 200:
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
        logger.warning(f"⚠️  エラー ({type(e).__name__}): {url} - {e}")
        return None

# ===== 電話番号抽出 =====
def extract_phone_from_tel_link(soup):
    """tel: リンクから電話番号抽出"""
    tel_links = soup.find_all('a', href=re.compile(r'^tel:'))
    for link in tel_links:
        phone = link.get('href', '').replace('tel:', '').strip()
        if is_valid_phone(phone):
            return phone
    return None

def extract_phone_from_regex(html_text):
    """正規表現で電話番号抽出"""
    for pattern in PHONE_PATTERNS:
        matches = re.findall(pattern, html_text)
        for match in matches:
            if is_valid_phone(match):
                return match
    return None

def extract_phone_from_jsonld(soup):
    """JSON-LD から電話番号抽出"""
    try:
        script_tags = soup.find_all('script', {'type': 'application/ld+json'})
        for script in script_tags:
            data = json.loads(script.string)
            if 'telephone' in data:
                phone = data['telephone']
                if is_valid_phone(phone):
                    return phone
    except Exception as e:
        logger.debug(f"JSON-LD パース エラー: {e}")
    return None

def extract_phone(html_text):
    """複合的な電話番号抽出"""
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # 優先度順：tel リンク → JSON-LD → 正規表現
    phone = extract_phone_from_tel_link(soup)
    if phone:
        logger.info(f"   📞 tel リンク: {phone}")
        return phone
    
    phone = extract_phone_from_jsonld(soup)
    if phone:
        logger.info(f"   📞 JSON-LD: {phone}")
        return phone
    
    phone = extract_phone_from_regex(html_text)
    if phone:
        logger.info(f"   📞 正規表現: {phone}")
        return phone
    
    return None

# ===== 企業名抽出 =====
def extract_company_name(html_text, url, crm_company_name=None):
    """HTML から企業名抽出"""
    if crm_company_name:
        return crm_company_name
    
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # og:site_name
    og_site_name = soup.find('meta', {'property': 'og:site_name'})
    if og_site_name and og_site_name.get('content'):
        return og_site_name['content']
    
    # H1 タグ
    h1 = soup.find('h1')
    if h1 and h1.text.strip():
        return h1.text.strip()
    
    domain = urlparse(url).netloc.replace('www.', '')
    return domain

# ===== クロール実行 =====
def crawl_domain(base_url, max_pages=5):
    """同一ドメイン内をクロール（優先パス優先）"""
    visited = set()
    to_visit = [base_url]
    all_html = []
    
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        
        if url in visited:
            continue
        
        visited.add(url)
        logger.info(f"   🔗 クロール: {url}")
        
        html = fetch_html(url)
        if html:
            all_html.append(html)
            
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                new_url = urljoin(url, link['href'])
                new_domain = urlparse(new_url).netloc
                base_domain = urlparse(base_url).netloc
                
                if new_domain == base_domain and new_url not in visited:
                    to_visit.append(new_url)
        
        time.sleep(0.5)
    
    return all_html

# ===== Scrape メイン =====
def scrape_website(url_data):
    """Web サイト情報をスクレイピング"""
    url = url_data['website_url']
    crm_company_name = url_data.get('company_name', '')
    
    logger.info(f"\n🌐 スクレイピング開始: {url}")
    
    # スキップ判定
    if should_skip_url(url):
        return {
            'company_name': crm_company_name,
            'phone_number': '',
            'status': 'skipped',
            'url': url
        }
    
    # HTML 取得
    html = fetch_html(url)
    if not html:
        logger.info(f"   ❌ HTML 取得失敗")
        return {
            'company_name': crm_company_name,
            'phone_number': '',
            'status': 'invalid',
            'url': url
        }
    
    # クロール
    logger.info(f"   📂 同一ドメイン内クロール開始")
    all_html = crawl_domain(url, max_pages=5)
    all_html.insert(0, html)
    
    # 企業名抽出
    company_name = extract_company_name(all_html[0], url, crm_company_name)
    logger.info(f"   🏢 企業名: {company_name}")
    
    # 電話番号抽出
    phone_number = None
    for page_html in all_html:
        phone_number = extract_phone(page_html)
        if phone_number:
            break
    
    # Status 判定
    if phone_number:
        status = 'ready_to_contact'
        logger.info(f"   ✅ status: ready_to_contact")
    else:
        status = 'invalid'
        logger.info(f"   ❌ status: invalid (電話番号なし)")
    
    return {
        'company_name': company_name,
        'phone_number': phone_number or '',
        'status': status,
        'url': url
    }

# ===== バッチ処理 =====
def run_batch_scraping(limit=None):
    """バッチスクレイピング実行"""
    logger.info("="*80)
    logger.info("🚀 batch scraping 開始")
    logger.info("="*80)
    
    url_list = read_website_urls_from_crm(limit=limit)
    
    if not url_list:
        logger.error("❌ URL リストが空です")
        return
    
    success_count = 0
    
    for idx, url_data in enumerate(url_list, start=1):
        try:
            result = scrape_website(url_data)
            
            if append_to_gsheet_phase5(
                result['company_name'],
                result['phone_number'],
                result['status'],
                result['url']
            ):
                if result['status'] == 'ready_to_contact':
                    success_count += 1
        
        except Exception as e:
            logger.error(f"❌ エラー (URL {idx}): {e}")
        
        logger.info(f"📊 進捗: {idx}/{len(url_list)}")
    
    logger.info("="*80)
    logger.info(f"✅ 処理完了: {len(url_list)} 件中 {success_count} 件で電話番号を取得")
    logger.info("="*80)

# ===== メイン関数 =====
def main():
    """エントリーポイント"""
    setup_logging()
    
    limit = None
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--limit'):
                try:
                    limit = int(arg.split('=')[1] if '=' in arg else sys.argv[sys.argv.index(arg) + 1])
                except (ValueError, IndexError):
                    logger.warning("⚠️  --limit の値が無効です")
    
    logger.info(f"📋 オプション: limit={limit}")
    
    run_batch_scraping(limit=limit)

# ===== エントリーポイント =====
if __name__ == "__main__":
    main()