import re, logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def extract_company_name(html_text, website_url, crm_company_name=None):
    """Return company name using priority: CRM value → <title> → <meta property='og:site_name'> → domain → 'Unknown'."""
    # crm_company_name が存在し、空でなければそれを使用
    if crm_company_name:
        # 型チェック：整数や他の型を文字列に変換
        crm_name_str = str(crm_company_name).strip()
        if crm_name_str and crm_name_str != 'None':
            logger.debug(f'✅ CRM から取得: {crm_name_str}')
            return crm_name_str
    
    # HTML から <title> を抽出
    soup = BeautifulSoup(html_text, 'html.parser')
    title = soup.find('title')
    if title and title.string:
        title_str = title.string.strip()
        logger.debug(f'📝 タイトルから抽出: {title_str}')
        return title_str
    
    # og:site_name メタタグから抽出
    og = soup.find('meta', property='og:site_name')
    if og and og.get('content'):
        og_str = og.get('content').strip()
        logger.debug(f'📝 og:site_name から抽出: {og_str}')
        return og_str
    
    # ドメインから抽出
    m = re.search(r'https?://(?:www\.)?([^/]+)', website_url)
    if m:
        domain = m.group(1)
        logger.debug(f'📝 ドメインから抽出: {domain}')
        return domain
    
    logger.warning('❌ 会社名抽出失敗、デフォルト値を使用')
    return 'Unknown'
