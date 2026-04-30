import re

with open('tools/email_extractor.py', 'r', encoding='utf-8') as f:
    content = f.read()

# is_valid_email 関数を探して、除外ロジックを追加
old_pattern = r'''def is_valid_email\(email\):
    """メールアドレスの有効性をチェック"""
    # ドメインチェック
    if '@' not in email:
        return False

    domain = email.split('@')[1].lower()

    # テスト用ドメインを除外
    invalid_domains = \[
        'example.com',
        'test.com',
        'sample.com',
        'localhost',
        'invalid.com',
        'example.org',
        'example.net',
    \]

    if domain in invalid_domains:
        return False

    return True'''

new_pattern = '''def is_valid_email(email):
    """メールアドレスの有効性をチェック"""
    # ドメインチェック
    if '@' not in email:
        return False

    domain = email.split('@')[1].lower()

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
        return False

    # サンプル・例示メールを除外
    local_part = email.split('@')[0].lower()
    sample_keywords = ['sample', 'example', 'test', 'demo', 'dummy']
    if any(keyword in local_part for keyword in sample_keywords):
        return False

    return True'''

content = re.sub(old_pattern, new_pattern, content, flags=re.DOTALL)

with open('tools/email_extractor.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ email_extractor.py を修正しました（sample/exampleメール除外）')
