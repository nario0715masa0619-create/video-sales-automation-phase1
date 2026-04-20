"""
company_info_extractor.py
企業名・メタ情報抽出
"""

import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def extract_company_name(html_text, url, crm_company_name=None):
    """HTML から企業名抽出"""
    # CRM のデータを優先
    if crm_company_name:
        return crm_company_name
    
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # og:site_name
        og_site_name = soup.find('meta', {'property': 'og:site_name'})
        if og_site_name and og_site_name.get('content'):
            return og_site_name['content']
        
        # og:title
        og_title = soup.find('meta', {'property': 'og:title'})
        if og_title and og_title.get('content'):
            return og_title['content']
        
        # title タグ
        title = soup.find('title')
        if title and title.text.strip():
            return title.text.strip()
        
        # H1 タグ
        h1 = soup.find('h1')
        if h1 and h1.text.strip():
            return h1.text.strip()
    except Exception as e:
        logger.debug(f"企業名抽出エラー: {e}")
    
    # フォールバック：ドメイン名から推測
    domain = urlparse(url).netloc.replace('www.', '')
    return domain

def extract_description(html_text):
    """メタディスクリプション抽出"""
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # og:description
        og_desc = soup.find('meta', {'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            return og_desc['content']
        
        # description
        desc = soup.find('meta', {'name': 'description'})
        if desc and desc.get('content'):
            return desc['content']
    except Exception as e:
        logger.debug(f"ディスクリプション抽出エラー: {e}")
    
    return None