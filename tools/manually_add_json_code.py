with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 180行目から187行目を置換
new_lines = []
skip_until = -1

for i, line in enumerate(lines):
    if i == 179:  # 180行目（0ベース）
        # JSON 読込コードを挿入
        new_lines.append('''    # Step 6 直前：JSON からメール情報を読み込んで割り当て
    import json
    email_data = {}
    if os.path.exists("cache/email_data.json"):
        with open("cache/email_data.json", "r", encoding="utf-8") as f:
            email_data = json.load(f)
    
    # scored_channels にメール情報を割り当て
    for ch in scored_channels:
        if ch.channel_url in email_data:
            ch.contact_email = email_data[ch.channel_url].get('email', '')
            ch.website_url = email_data[ch.channel_url].get('website', '')
            ch.contact_form_url = email_data[ch.channel_url].get('form_url', '')
    
    logger.info(f"✅ メール情報読込: JSON から {len(email_data)} 件を読み込み")

    # デバッグ：読み込んだデータの確認
    logger.info("=== メール情報割り当て後（最初の3件） ===")
    for i, ch in enumerate(scored_channels[:3]):
        logger.info(f"{i+1}. {ch.channel_name}: email='{ch.contact_email}', website='{ch.website_url}'")

''')
        skip_until = 188  # 189行目まで（0ベース）スキップ
    elif i >= skip_until:
        new_lines.append(line)
    elif i < 179:
        new_lines.append(line)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ JSON 読込コードを手動で追加しました')
