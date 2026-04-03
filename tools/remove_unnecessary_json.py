with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 不要な JSON 読込・割り当てコードを削除（186-198行目相当）
old_code = '''    logger.info(f"✅ メール情報保存: {len(email_data)} 件 を JSON に保存")

    # Step 6 直前：JSON からメール情報を読み込んで割り当て
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
        logger.info(f"{i+1}. {ch.channel_name}: email='{ch.contact_email}', website='{ch.website_url}'")'''

new_code = '''    logger.info(f"✅ メール情報保存: {len(email_data)} 件 を JSON に保存")'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ 不要な JSON 読込・割り当てコードを削除しました')
