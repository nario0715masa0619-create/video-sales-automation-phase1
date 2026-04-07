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

# データ検証関数（CRM保存データの確認用）
def validate_crm_data_saved(min_email_ratio=0.8):
    """
    Google Sheets にメール情報が実際に保存されたか検証する
    
    Args:
        min_email_ratio: メール情報を持つリードの最小割合（デフォルト 0.8 = 80%）
    
    Returns:
        tuple: (メール情報を持つリード数, 総リード数)
    
    Raises:
        Exception: メール情報が保存されていない場合
    """
    from crm_manager import CRMManager
    
    crm = CRMManager()
    leads = crm.get_all_leads()
    
    with_email = sum(1 for lead in leads if lead.get('メールアドレス'))
    total = len(leads)
    
    if total == 0:
        return 0, 0
    
    email_ratio = with_email / total if total > 0 else 0
    
    if email_ratio < min_email_ratio:
        raise Exception(
            f"❌ メール情報の検証エラー\n"
            f"   総リード数: {total} 件\n"
            f"   メール情報あり: {with_email} 件\n"
            f"   比率: {email_ratio*100:.1f}% (最小: {min_email_ratio*100:.0f}%)\n"
            f"   原因: Step 6 と Step 7 の順序を確認してください\n"
            f"   詳細: CHECKLIST.md のトラブルシューティングを参照"
        )
    
    return with_email, total
