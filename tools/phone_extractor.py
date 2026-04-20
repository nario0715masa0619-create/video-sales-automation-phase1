"""
phone_extractor.py
電話番号抽出ロジック（複数の方法で抽出を試みる）
"""
import logging
import re
import json
from bs4 import BeautifulSoup
from config import PHONE_PATTERNS

logger = logging.getLogger(__name__)

def is_valid_phone(phone_str):
    """日本の電話番号の妥当性チェック（厳密版）"""
    if not phone_str:
        return False

    original_phone = phone_str  # オリジナルを保存（国際電話用）

    # **国際電話（+81）は先に確認**
    if phone_str.startswith('+81'):
        if re.match(r'^\+81\d{9,11}$', phone_str):
            logger.debug(f"✅ 有効な電話番号（国際）: {phone_str}")
            return True
        else:
            logger.debug(f"❌ 無効な国際電話形式: {phone_str}")
            return False

    # 空白やハイフン、括弧を削除（国際電話以外）
    cleaned = re.sub(r'[\s\-\(\)]', '', phone_str)

    # 数字のみか確認
    if not re.fullmatch(r'\d+', cleaned):
        return False

    # **00 で始まる番号は国際電話プレフィックス → 除外**
    if cleaned.startswith('00'):
        logger.debug(f"❌ 無効（00プレフィックス）: {phone_str}")
        return False

    # **02 で始まる番号は不正な市外局番 → 除外**
    if cleaned.startswith('02'):
        logger.debug(f"❌ 無効（02市外局番は実在しない）: {phone_str}")
        return False

    # 長さチェック（10-13桁）
    if len(cleaned) < 10 or len(cleaned) > 13:
        logger.debug(f"❌ 無効（長さ不正）: {phone_str} ({len(cleaned)}桁)")
        return False

    # 同じ数字の繰り返し（0000000000など）を除外
    if len(set(cleaned)) == 1:
        logger.debug(f"❌ 無効（同一数字繰り返し）: {phone_str}")
        return False

    # **厳密な日本の電話番号パターン**
    valid_patterns = [
        # 携帯・PHS: 070/080/090 + 8桁 = 11桁
        r'^(070|080|090)\d{8}$',

        # 固定電話パターン（厳密版）
        # 03XXXXXXXX（東京、10桁）
        r'^03\d{8}$',
        # 06XXXXXXXX（大阪、10桁）
        r'^06\d{8}$',
        # 011XXXXXXX（札幌、11桁）
        r'^011\d{7}$',
        # その他の固定電話: 0X + 8-9桁 (合計10-11桁)
        r'^0[1-9]\d{8}$',
        r'^0[1-9]\d{9}$',

        # フリーダイヤル: 0120 + 6-8桁 = 10-12桁
        r'^0120\d{6,8}$',

        # ナビダイヤル: 0570 + 6-8桁 = 10-12桁
        r'^0570\d{6,8}$',
    ]

    for pattern in valid_patterns:
        if re.match(pattern, cleaned):
            logger.debug(f"✅ 有効な電話番号: {phone_str} ({len(cleaned)}桁)")
            return True

    logger.debug(f"❌ 無効な電話番号形式: {phone_str} ({len(cleaned)}桁)")
    return False

def extract_phone_from_tel_link(soup):
    """<a href="tel:xxx"> から抽出"""
    for a in soup.find_all('a', href=re.compile(r'^tel:')):
        phone = a.get('href', '').replace('tel:', '').strip()
        if is_valid_phone(phone):
            return phone
    return None

def extract_phone_from_regex(html_text):
    """正規表現で抽出"""
    for pat in PHONE_PATTERNS:
        for m in re.findall(pat, html_text):
            if is_valid_phone(m):
                return m
    return None

def extract_phone_from_jsonld(soup):
    """JSON-LD スキーマから抽出"""
    try:
        for s in soup.find_all('script', {'type': 'application/ld+json'}):
            data = json.loads(s.string)
            if isinstance(data, dict) and 'telephone' in data:
                phone = data['telephone']
                if is_valid_phone(phone):
                    return phone
    except Exception as e:
        logger.debug(f"JSON-LD パース エラー: {e}")
    return None

def extract_phone_from_meta(soup):
    """メタタグから抽出"""
    for m in soup.find_all('meta'):
        attr = m.get('property') or m.get('name')
        if attr and 'phone' in attr.lower():
            phone = m.get('content', '').strip()
            if is_valid_phone(phone):
                return phone
    return None

def extract_phone(html_text):
    """複数の方法で電話番号を抽出（優先度順）"""
    soup = BeautifulSoup(html_text, 'html.parser')

    # 1. tel リンク
    phone = extract_phone_from_tel_link(soup)
    if phone:
        logger.info(f"   📞 tel リンク: {phone}")
        return phone

    # 2. JSON-LD
    phone = extract_phone_from_jsonld(soup)
    if phone:
        logger.info(f"   📞 JSON-LD: {phone}")
        return phone

    # 3. メタタグ
    phone = extract_phone_from_meta(soup)
    if phone:
        logger.info(f"   📞 メタタグ: {phone}")
        return phone

    # 4. 正規表現
    phone = extract_phone_from_regex(html_text)
    if phone:
        logger.info(f"   📞 正規表現: {phone}")
        return phone

    return None