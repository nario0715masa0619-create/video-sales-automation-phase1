"""
email_extractor.py
メールアドレス抽出ロジック（複数の方法で抽出を試みる）
"""
import logging
import re
import json
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def is_valid_email(email_str):
    """メールアドレスの妥当性チェック"""
    if not email_str:
        return False
    
    # 基本的なメールアドレス正規表現
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email_str):
        logger.debug(f"❌ 無効なメールアドレス形式: {email_str}")
        return False
    
    # ドメイン部分を抽出
    domain = email_str.split('@')[1].lower()
    
    # テスト用ドメインを除外
    invalid_domains = [
        'example.com',
        'test.com',
        'sample.com',
        'localhost',
        'invalid.com',
        'example.org',
        'example.net',
    ]
    
    if domain in invalid_domains:
        logger.debug(f"❌ テスト用ドメイン除外: {email_str}")
        return False
    
    # よくある誤字ドメインを除外
    common_typos = {
        'gmial.com': 'gmail.com',
        'gmai.com': 'gmail.com',
        'yahooo.com': 'yahoo.com',
        'hotmial.com': 'hotmail.com',
    }
    
    if domain in common_typos:
        logger.debug(f"❌ 誤字ドメイン除外: {email_str} (正: {common_typos[domain]})")
        return False
    
    logger.debug(f"✅ 有効なメールアドレス: {email_str}")
    return True

def extract_email_from_mailto_link(soup):
    """<a href="mailto:xxx"> から抽出"""
    for a in soup.find_all('a', href=re.compile(r'^mailto:')):
        email = a.get('href', '').replace('mailto:', '').strip()
        if is_valid_email(email):
            return email
    return None

def extract_email_from_regex(html_text):
    """正規表現で抽出"""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(pattern, html_text)
    for email in matches:
        if is_valid_email(email):
            return email
    return None

def extract_email_from_jsonld(soup):
    """JSON-LD スキーマから抽出"""
    try:
        for s in soup.find_all('script', {'type': 'application/ld+json'}):
            data = json.loads(s.string)
            if isinstance(data, dict):
                # email フィールドを探す
                if 'email' in data:
                    email = data['email']
                    if is_valid_email(email):
                        return email
                # contactPoint.email を探す
                if 'contactPoint' in data:
                    contact = data['contactPoint']
                    if isinstance(contact, dict) and 'email' in contact:
                        email = contact['email']
                        if is_valid_email(email):
                            return email
    except Exception as e:
        logger.debug(f"JSON-LD パース エラー: {e}")
    return None

def extract_email_from_meta(soup):
    """メタタグから抽出"""
    for m in soup.find_all('meta'):
        attr = m.get('property') or m.get('name')
        if attr and 'email' in attr.lower():
            email = m.get('content', '').strip()
            if is_valid_email(email):
                return email
    return None

def extract_email(html_text):
    """複数の方法でメールアドレスを抽出（優先度順）"""
    soup = BeautifulSoup(html_text, 'html.parser')

    # 1. mailto リンク
    email = extract_email_from_mailto_link(soup)
    if email:
        logger.info(f"   📧 mailto リンク: {email}")
        return email

    # 2. JSON-LD
    email = extract_email_from_jsonld(soup)
    if email:
        logger.info(f"   📧 JSON-LD: {email}")
        return email

    # 3. メタタグ
    email = extract_email_from_meta(soup)
    if email:
        logger.info(f"   📧 メタタグ: {email}")
        return email

    # 4. 正規表現
    email = extract_email_from_regex(html_text)
    if email:
        logger.info(f"   📧 正規表現: {email}")
        return email

    return None
