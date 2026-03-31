"""
email_extractor.py
YouTubeチャンネルの公式サイトからメールアドレスを自動取得する
方式：
  1. yt-dlp でチャンネル説明文からサイトURLを抽出
  2. HTMLのytInitialDataからサイトURLを抽出（フォールバック）
  3. 取得したサイトのお問い合わせページからメールを抽出
"""

import re
import json
import time
import logging
import requests
import yt_dlp
from urllib.parse import urlparse, urljoin
from utils import normalize_url
from bs4 import BeautifulSoup

REQUEST_TIMEOUT = 10
MAX_CRAWL_PAGES = 6

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'ja-JP,ja;q=0.9,en;q=0.8',
}

EMAIL_PATTERN = re.compile(
    r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
)

# 除外ドメイン（SNS・YouTube等）
EXCLUDE_DOMAINS = [
    'youtube.com', 'youtu.be', 'instagram.com', 'twitter.com',
    'x.com', 'facebook.com', 't.co', 'tiktok.com', 'line.me',
    'ameblo.jp', 'note.com', 'linktr.ee', 'lit.link',
    'google.com', 'apple.com', 'microsoft.com',
]

# 除外メールキーワード
EXCLUDE_EMAIL_KEYWORDS = [
    'example', 'test', 'noreply', 'no-reply',
    'sentry', 'wixpress', 'wordpress', 'schema',
    '.png', '.jpg', '.gif', '.svg', '.webp',
]


def _find_values_recursive(data, target_key: str) -> list:
    """JSONを再帰的に検索して指定キーの値を全て返す"""
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                results.append(value)
            else:
                results.extend(_find_values_recursive(value, target_key))
    elif isinstance(data, list):
        for item in data:
            results.extend(_find_values_recursive(item, target_key))
    return results


def _get_website_via_ytdlp(base_url: str) -> str:
    """yt-dlpでチャンネル説明文からサイトURLを抽出"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'playlistend': 1,
        'ignoreerrors': True,
        'socket_timeout': 20,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(base_url, download=False)
        if not info:
            return ""

        description = info.get('description', '') or ''
        urls = re.findall(r'https?://[^\s\)\"\'\u3000\u3001\u3002]+', description)

        for url in urls:
            url = url.rstrip('.,)')
            if not any(d in url for d in EXCLUDE_DOMAINS):
                logger.info(f"yt-dlp でサイトURL発見: {url}")
                return url
    except Exception as e:
        logger.debug(f"yt-dlp サイトURL取得失敗: {e}")
    return ""


def _get_website_via_html(base_url: str) -> str:
    """YouTubeのaboutページHTMLからサイトURLを抽出"""
    about_url = base_url.rstrip('/') + '/about'
    try:
        resp = requests.get(about_url, headers=HEADERS, timeout=15)
        html = resp.text

        # ytInitialDataのJSONをパース
        match = re.search(
            r'(?:var ytInitialData|ytInitialData)\s*=\s*({.+?});\s*(?:var |window\[|</script>)',
            html, re.DOTALL
        )
        if match:
            try:
                data = json.loads(match.group(1))
                # channelExternalLinkViewModelを再帰検索
                links = _find_values_recursive(data, 'channelExternalLinkViewModel')
                for link in links:
                    url = ''
                    if isinstance(link, dict):
                        url = (link.get('link') or {}).get('content', '')
                        if not url:
                            url = (link.get('navigationEndpoint') or {}).get('urlEndpoint', {}).get('url', '')

                    if url and not any(d in url for d in EXCLUDE_DOMAINS):
                        if not url.startswith('http'):
                            url = 'https://' + url
                        logger.info(f"ytInitialData でサイトURL発見: {url}")
                        return url

            except json.JSONDecodeError:
                pass

        # フォールバック：直接正規表現でHTMLからURL検索
        patterns = [
            r'"canonicalBaseUrl":"(https?://[^"]+)"',
            r'"targetUrl":"(https?://(?!(?:www\.)?youtube)[^"]+)"',
        ]
        for pattern in patterns:
            m = re.search(pattern, html)
            if m:
                url = m.group(1)
                if not any(d in url for d in EXCLUDE_DOMAINS):
                    logger.info(f"HTML正規表現でサイトURL発見: {url}")
                    return url
    except Exception as e:
        logger.debug(f"HTML サイトURL取得失敗: {e}")
    return ""


def get_website_from_youtube(base_url: str) -> str:
    """
    YouTubeチャンネルURLから公式サイトURLを取得する
    1. yt-dlp（説明文）→ 2. HTML解析 の順で試みる
    """
    # 方法1: yt-dlp
    website = _get_website_via_ytdlp(base_url)
    if website:
        return website

    # 方法2: HTML解析
    website = _get_website_via_html(base_url)
    if website:
        return website

    logger.warning(f"公式サイトURL取得失敗: {base_url}")
    return ""


def scrape_email_from_site(website_url: str) -> tuple:
    """
    企業サイトからメールアドレスとお問い合わせフォームURLを抽出する
    Returns: (email: str, contact_form_url: str)
    """
    parsed = urlparse(website_url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    contact_form_keywords = ['contact', 'inquiry', 'support', 'help', 'toiawase', 'form']
    contact_text_keywords = ['お問い合わせ', 'お問合せ', '資料請求', 'お問い合わせはこちら', 'contact']
    
    # 試みるページのパス一覧（バックアップ用）
    candidate_paths = [
        '',
        '/contact', '/contact.html', '/contact/',
        '/inquiry', '/inquiry.html', '/inquiry/',
        '/about', '/about.html',
        '/company', '/company.html', '/company/profile',
        '/corporate', '/corporate/contact',
        '/support', '/help',
    ]

    contact_form_url = ''
    crawled_count = 0

    def _extract_emails_from_text(text: str) -> list:
        # 簡易obfuscation対応
        t = text.replace('[at]', '@').replace('(at)', '@').replace('＠', '@')
        emails = EMAIL_PATTERN.findall(t)
        return [
            e for e in emails
            if not any(kw in e.lower() for kw in EXCLUDE_EMAIL_KEYWORDS)
        ]

    def _select_best_email(emails: list) -> str:
        if not emails:
            return ""
        domain = parsed.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        domain_emails = [e for e in emails if e.lower().endswith('@' + domain.lower())]
        if domain_emails:
            return domain_emails[0]
        role_emails = [e for e in emails if any(e.lower().startswith(prefix) for prefix in ['info@', 'sales@', 'support@', 'contact@'])]
        if role_emails:
            return role_emails[0]
        return emails[0]

    contact_links = []

    # --- 1. TOPページを取得 ---
    try:
        resp = requests.get(base, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        crawled_count += 1
        
        if resp.status_code == 200:
            html = resp.text
            found_email = ""
            
            # BeautifulSoup でリンク解析
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text(strip=True)
                
                # mailto: のチェック
                if href.lower().startswith('mailto:'):
                    mailto_addr = href[7:].split('?')[0].strip()
                    mailto_addr = mailto_addr.replace('[at]', '@').replace('(at)', '@').replace('＠', '@')
                    if EMAIL_PATTERN.match(mailto_addr):
                        if not any(kw in mailto_addr.lower() for kw in EXCLUDE_EMAIL_KEYWORDS):
                            found_email = mailto_addr
                            
                # 絶対URL化
                abs_url = urljoin(base, href)
                parsed_abs = urlparse(abs_url)
                
                # 問い合わせ系リンクの判定
                url_lower = abs_url.lower()
                text_lower = text.lower()
                
                is_contact = any(kw in url_lower for kw in contact_form_keywords) or \
                             any(kw in text_lower for kw in [k.lower() for k in contact_text_keywords])
                             
                if is_contact:
                    if not contact_form_url:
                        contact_form_url = normalize_url(abs_url)
                        logger.info(f"フォームのみ発見 ({contact_form_url})")

                    # 同一ドメイン（サブドメイン含む簡易判定）を優先
                    if parsed.netloc in parsed_abs.netloc or parsed_abs.netloc in parsed.netloc:
                        if abs_url not in [link['url'] for link in contact_links] and abs_url != base:
                            contact_links.append({'url': abs_url, 'priority': 1})
                    else:
                        if abs_url not in [link['url'] for link in contact_links] and abs_url != base:
                            contact_links.append({'url': abs_url, 'priority': 2})

            if found_email:
                # Markdown形式等が含まれていないか念のためクリーニング
                found_email = re.sub(r'\[(.*?)\]\(mailto:.*?\)', r'\1', found_email)
                logger.info(f"メール発見 ({base}): {found_email}")
                return found_email, contact_form_url

            # テキストからのメール抽出 (TOP)
            emails = _extract_emails_from_text(html)
            best_email = _select_best_email(emails)
            if best_email:
                best_email = re.sub(r'\[(.*?)\]\(mailto:.*?\)', r'\1', best_email)
                logger.info(f"メール発見 ({base}): {best_email}")
                return best_email, contact_form_url

    except Exception as e:
        logger.debug(f"TOPページクロール失敗 ({base}): {e}")

    # contact_links を優先度とURL長でソート（同じ優先度なら短いURLを優先）
    contact_links.sort(key=lambda x: (x['priority'], len(x['url'])))
    candidate_urls = [link['url'] for link in contact_links[:4]] # 最大4件
    
    logger.info(f"問い合わせ候補リンク: {len(contact_links)}件")
    
    # --- 2. 問い合わせ系リンクを巡回 ---
    for url in candidate_urls:
        if crawled_count >= MAX_CRAWL_PAGES:
            break
            
        time.sleep(0.1)
        try:
            r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            crawled_count += 1
            if r.status_code == 200:
                # ページ内からもメールを探す
                soup = BeautifulSoup(r.text, 'html.parser')
                found_email = ""
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.lower().startswith('mailto:'):
                        mailto_addr = href[7:].split('?')[0].strip()
                        mailto_addr = mailto_addr.replace('[at]', '@').replace('(at)', '@').replace('＠', '@')
                        if EMAIL_PATTERN.match(mailto_addr):
                            if not any(kw in mailto_addr.lower() for kw in EXCLUDE_EMAIL_KEYWORDS):
                                found_email = mailto_addr
                                break

                if found_email:
                    found_email = re.sub(r'\[(.*?)\]\(mailto:.*?\)', r'\1', found_email)
                    logger.info(f"メール発見 ({url}): {found_email}")
                    return found_email, contact_form_url
                    
                emails = _extract_emails_from_text(r.text)
                best_email = _select_best_email(emails)
                if best_email:
                    best_email = re.sub(r'\[(.*?)\]\(mailto:.*?\)', r'\1', best_email)
                    logger.info(f"メール発見 ({url}): {best_email}")
                    return best_email, contact_form_url
                    
                # フォームURLの補完
                if not contact_form_url and any(kw in url.lower() for kw in contact_form_keywords):
                    contact_form_url = normalize_url(url)
                    logger.info(f"フォームのみ発見 ({contact_form_url})")
        except Exception as e:
            logger.debug(f"クロール失敗 ({url}): {e}")

    # --- 3. バックアップ（candidate_paths の総当り） ---
    for path in candidate_paths:
        if crawled_count >= MAX_CRAWL_PAGES:
            break
            
        url = base + path
        if url == base or url in candidate_urls: 
            continue
            
        time.sleep(0.1)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            crawled_count += 1
            if resp.status_code != 200:
                continue

            emails = _extract_emails_from_text(resp.text)
            best_email = _select_best_email(emails)
            if best_email:
                best_email = re.sub(r'\[(.*?)\]\(mailto:.*?\)', r'\1', best_email)
                logger.info(f"メール発見 ({url}): {best_email}")
                return best_email, contact_form_url

            if not contact_form_url and any(kw in url.lower() for kw in contact_form_keywords):
                contact_form_url = normalize_url(url)
                logger.info(f"フォームのみ発見 ({contact_form_url})")

        except Exception as e:
            logger.debug(f"クロール失敗 ({url}): {e}")

    logger.info(f"メール未発見。フォームURL: {contact_form_url or 'なし'}")
    return '', contact_form_url


def get_email_from_youtube_channel(base_url: str) -> tuple:
    """
    YouTubeチャンネルURLから (website_url, email, contact_form_url) を取得する
    """
    website_url = get_website_from_youtube(base_url)
    if not website_url:
        return "", "", ""

    email, contact_form_url = scrape_email_from_site(website_url)
    return website_url, email, contact_form_url


# 単体テスト用
if __name__ == '__main__':
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s'
    )

    test_channels = sys.argv[1:] if len(sys.argv) > 1 else [
        'https://www.youtube.com/@netschoolcorp',
        'https://www.youtube.com/@AskulOfficial',
    ]

    for ch_url in test_channels:
        print(f"\n{'='*50}")
        print(f"検索中: {ch_url}")
        website, email, form_url = get_email_from_youtube_channel(ch_url)
        print(f"  公式サイト:       {website or '取得失敗'}")
        print(f"  メール:           {email or '未発見'}")
        print(f"  お問い合わせURL:  {form_url or '未発見'}")


