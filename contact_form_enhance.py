def _extract_contact_form_url(html: str, base_url: str) -> str:
    """HTML から contact form URL を抽出"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # パターン1: <form action="..."> を検出
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action', '')
            if action:
                if action.startswith('http'):
                    return action
                else:
                    return urljoin(base_url, action)
        
        # パターン2: お問い合わせリンクを検出
        contact_links = soup.find_all('a', href=True)
        for link in contact_links:
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            if any(kw in href or kw in text for kw in ['contact', 'inquiry', 'お問い合わせ', 'お問合せ', 'contact-form', 'form']):
                url = link.get('href', '')
                if url.startswith('http'):
                    return url
                elif url.startswith('/'):
                    return urljoin(base_url, url)
        
        return ''
    except Exception as e:
        logger.debug(f"Contact Form 抽出エラー: {e}")
        return ''
