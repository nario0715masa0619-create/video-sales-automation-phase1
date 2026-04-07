with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 192-198行目（ループ直前の JSON 読込）を削除
old_code = '''    if not dry_run:
        # JSON からメール情報を再度読み込む（ループ開始直前）
        import json
        email_data_loop = {}
        if os.path.exists("cache/email_data.json"):
            with open("cache/email_data.json", "r", encoding="utf-8") as f:
                email_data_loop = json.load(f)
        
        for i, ch in enumerate(scored_channels):'''

new_code = '''    if not dry_run:
        for i, ch in enumerate(scored_channels):'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ ループ内の不要な JSON 読込コードを削除しました')
