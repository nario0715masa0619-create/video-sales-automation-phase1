with open('tools/email_extractor.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 59行目（return True の前）に挿入
insert_code = '''
    # サンプル・例示メールを除外
    local_part = email_str.split('@')[0].lower()
    sample_keywords = ['sample', 'example', 'test', 'demo', 'dummy']
    if any(keyword in local_part for keyword in sample_keywords):
        logger.debug(f"❌ サンプルメール除外: {email_str}")
        return False
'''

# 59行目（0-indexed では 58）の前に挿入
lines.insert(58, insert_code)

with open('tools/email_extractor.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ email_extractor.py にサンプルメール除外ロジックを追加しました')
