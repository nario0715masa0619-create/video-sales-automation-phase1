with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# JSON 読込コードを正しく追加
old_code = '''    # Step 6 直前：キャッシュから scored_channels を再度読み込む
    # pickle は使用しないため削除
    logger.info(f"✅ キャッシュ読込: {len(scored_channels)} 件のメール情報を確認")

    # デバッグ：キャッシュから読み込んだデータの確認
    logger.info("=== キャッシュ読込後のメール情報（最初の3件） ===")
    for i, ch in enumerate(scored_channels[:3]):
        logger.info(f"{i+1}. {ch.channel_name}: email='{ch.contact_email}', website='{ch.website_url}'")'''

new_code = '''    # Step 6 直前：JSON からメール情報を読み込んで割り当て
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

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ JSON 読込コードを追加しました')
