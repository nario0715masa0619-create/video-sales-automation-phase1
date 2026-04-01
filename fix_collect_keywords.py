with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ハードコードされたキーワードを config から取得するよう修正
old_code = '''    # デフォルトキーワード
    if not keywords:
        keywords = [
            'YouTube 集客', 'セミナー YouTube', 'オンライン講座 YouTube',
            'ウェビナー YouTube', 'スクール YouTube', '教室 YouTube',
            'クリニック YouTube', 'ジム YouTube', '整体院 YouTube',
            '学習塾 YouTube', '士業 YouTube', 'コーチング YouTube'
        ]'''

new_code = '''    # デフォルトキーワード
    if not keywords:
        keywords = config.DEFAULT_SEARCH_KEYWORDS'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ collect.py をconfig.DEFAULT_SEARCH_KEYWORDS から取得するよう修正しました')
