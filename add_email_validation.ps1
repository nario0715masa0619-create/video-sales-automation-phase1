$filePath = "email_extractor.py"

# メールアドレス検証関数を追加
$validationCode = @'

import re
import dns.resolver

def is_valid_email_format(email):
    """基本的なメールアドレス形式チェック"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_domain(domain):
    """MXレコード確認（ドメインが実在するか）"""
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except Exception:
        return False

def is_valid_email(email):
    """メールアドレスの有効性チェック（形式 + ドメイン実在確認）"""
    if not is_valid_email_format(email):
        return False
    
    domain = email.split('@')[1]
    return is_valid_domain(domain)
'@

Write-Host "✅ メールアドレス検証機能を追加します" -ForegroundColor Green
