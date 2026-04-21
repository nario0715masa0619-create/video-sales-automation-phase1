# website_url_fetcher.py - URL 取得元を統一化

from typing import List, Tuple, Optional
import logging
from crm_manager import read_website_urls_from_crm

logger = logging.getLogger(__name__)

def get_website_urls(
    source: str = 'crm',
    limit: Optional[int] = None,
    **kwargs
) -> List[Tuple]:
    """
    複数のソースから website_url を取得
    
    Args:
        source: 'crm', 'google_search', 'file' など
        limit: 取得件数上限
        **kwargs: 各ソース固有のパラメータ
    
    Returns:
        List[Tuple]: [(idx, website_url, company_name), ...]
    """
    
    if source == 'crm':
        return _fetch_from_crm(limit=limit, **kwargs)
    elif source == 'google_search':
        return _fetch_from_google_search(**kwargs)
    elif source == 'file':
        return _fetch_from_file(**kwargs)
    else:
        raise ValueError(f"Unknown source: {source}")

def _fetch_from_crm(
    limit: Optional[int] = None,
    url_column: str = 'チャンネルURL',
    name_column: str = '会社名'
) -> List[Tuple]:
    """
    CRM から website_url を取得
    
    Args:
        limit: 取得件数上限
        url_column: URL を格納する列名（デフォルト: 'チャンネルURL'）
        name_column: 会社名を格納する列名（デフォルト: '会社名'）
    
    Returns:
        List[Tuple]: [(idx, website_url, company_name), ...]
    """
    logger.info(f"CRM から {url_column} を取得中...")
    urls = read_website_urls_from_crm(limit=limit)
    logger.info(f"✅ CRM から {len(urls)} 件取得")
    return urls

def _fetch_from_google_search(
    company_names: List[str],
    max_results: int = 3
) -> List[Tuple]:
    """
    Google 検索から website_url を取得（未実装）
    
    Args:
        company_names: 検索する会社名リスト
        max_results: 1 検索あたりの結果数
    """
    logger.warning("Google Search 機能は未実装です（Phase 5 で実装予定）")
    return []

def _fetch_from_file(
    filepath: str,
    url_column: str = 'website_url',
    name_column: str = 'company_name'
) -> List[Tuple]:
    """
    CSV/JSON ファイルから website_url を取得（未実装）
    
    Args:
        filepath: ファイルパス
        url_column: URL 列名
        name_column: 会社名列名
    """
    logger.warning("File 読み込み機能は未実装です（Phase 5 で実装予定）")
    return []

if __name__ == '__main__':
    # テスト: CRM から取得
    urls = get_website_urls(source='crm', limit=5)
    print(f"取得件数: {len(urls)}")
    for idx, url, email, company_name in urls:
        print(f"  {idx}: {company_name} - {url}")
