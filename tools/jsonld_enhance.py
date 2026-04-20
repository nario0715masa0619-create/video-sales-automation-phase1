def _extract_emails_from_jsonld_enhanced(html: str) -> list:
    """JSON-LD スキーマから email を完全抽出（Organization, LocalBusiness, contactPoint対応）"""
    emails = []
    soup = BeautifulSoup(html, 'html.parser')
    
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            ld_json = json.loads(script.string)
            
            # パターン1: 直接的な email フィールド
            if isinstance(ld_json, dict):
                direct_emails = _find_values_recursive(ld_json, 'email')
                emails.extend([e for e in direct_emails if isinstance(e, str) and '@' in e])
            
            # パターン2: contactPoint 内の email
            contact_points = _find_values_recursive(ld_json, 'contactPoint')
            for cp in contact_points:
                if isinstance(cp, dict):
                    if 'email' in cp:
                        emails.append(cp['email'])
                    elif 'contactPoint' in cp:
                        nested = cp['contactPoint']
                        if isinstance(nested, dict) and 'email' in nested:
                            emails.append(nested['email'])
            
            # パターン3: @type ごとの処理
            schema_type = ld_json.get('@type', '')
            if schema_type in ['Organization', 'LocalBusiness', 'CivicStructure']:
                # 各スキーマ固有のフィールドをチェック
                if 'sameAs' in ld_json:
                    # LinkedIn等から推測
                    pass
        except json.JSONDecodeError:
            continue
        except Exception as e:
            logger.debug(f"JSON-LD 解析エラー: {e}")
    
    # 重複排除とバリデーション
    valid_emails = []
    for email in set(emails):
        if EMAIL_PATTERN.match(email) or EMAIL_PATTERN_JP.match(email):
            valid_emails.append(email)
    
    return valid_emails
