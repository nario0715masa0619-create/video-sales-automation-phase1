with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 6 直前のキャッシュ読み込みを削除し、別の方法を使用
old_code = '''    # Step 6 直前：キャッシュから scored_channels を再度読み込む
    with open("cache/scored_channels.pkl", "rb") as f:
        scored_channels = pickle.load(f)
    logger.info(f"✅ キャッシュ読込: {len(scored_channels)} 件のメール情報を確認")

    # デバッグ：キャッシュから読み込んだデータの確認
    logger.info("=== キャッシュ読込後のメール情報（最初の3件） ===")
    for i, ch in enumerate(scored_channels[:3]):
        logger.info(f"{i+1}. {ch.channel_name}: email='{ch.contact_email}', website='{ch.website_url}'")'''

new_code = '''    # Step 6 直前：メール情報をロード（pickle ではなく dict で保存）
    import json
    email_data = {}
    if os.path.exists("cache/email_data.json"):
        with open("cache/email_data.json", "r", encoding="utf-8") as f:
            email_data = json.load(f)
    
    # scored_channels にメール情報を再度割り当て
    for ch in scored_channels:
        if ch.channel_url in email_data:
            ch.contact_email = email_data[ch.channel_url].get('email', '')
            ch.website_url = email_data[ch.channel_url].get('website', '')
            ch.contact_form_url = email_data[ch.channel_url].get('form_url', '')
    
    logger.info(f"✅ メール情報を読込: {len(email_data)} 件")'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ メール情報の保存方法を JSON に変更しました')
