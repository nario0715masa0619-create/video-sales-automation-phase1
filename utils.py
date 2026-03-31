"""
utils.py
========
プロジェクト全体で使用する共通ユーティリティ関数を定義するモジュール。
"""

import re
from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """
    URL の前後の空白と末尾の不要文字を除去する。
    
    HTML からのスクレイピングや正規表現マッチにより、
    末尾に括弧や句読点がゴミとして付く問題を防止する。
    
    Args:
        url (str): 正規化対象の URL
        
    Returns:
        str: 正規化済みの URL
        
    例：
        normalize_url("http://www.keieiryoku.jp/）")
        → "http://www.keieiryoku.jp/"
        
        normalize_url("http://example.com/form?id=123 ")
        → "http://example.com/form?id=123"
    """
    if not url:
        return url
    
    # 前後の空白・全角スペースを除去
    url = url.strip()
    
    # 末尾の不要文字を削除
    # （全角かっこ / 半角かっこ / 句読点 / カンマ / 全角スペース）
    url = url.rstrip("）)。、,　 ")
    
    return url


def is_valid_url(url: str) -> bool:
    """
    URL として有効かどうかを簡易判定する。
    
    Args:
        url (str): 判定対象の URL
        
    Returns:
        bool: 有効な URL の場合 True
    """
    if not url:
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
