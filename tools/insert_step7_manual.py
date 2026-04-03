with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 開始行を探す
insert_pos = -1
for i, line in enumerate(lines):
    if '# Step 6: CRM 更新' in line:
        insert_pos = i
        break

if insert_pos > 0:
    # Step 7 コードを挿入
    step7 = """    logger.info("\n=== Step 7: メールアドレス自動取得 ===")
    email_count = 0
    email_data = {}
    for i, ch in enumerate(scored_channels):
        if i % 10 == 0 and i > 0:
            logger.info(f"進捗: {i}/{len(scored_channels)}")

        channel_url = ch.channel.channel_url
        company_name = ch.channel.channel_name

        try:
            website_url, email, contact_form_url = get_email_from_youtube_channel(channel_url)
            ch.channel.contact_email = email if email else ""
            ch.channel.website_url = website_url if website_url else ""
            ch.channel.contact_form_url = contact_form_url if contact_form_url else ""
            if email:
                logger.info(f"✅ メール取得成功: {company_name} → {email}")
                email_count += 1
            else:
                logger.debug(f"メール取得失敗: {company_name}")
        except Exception as e:
            logger.warning(f"メール抽出エラー [{company_name}]: {e}")

    logger.info(f"✅ Step 7 完了: {email_count} 件のメール取得")

    # JSON にメール情報を保存
    os.makedirs("cache", exist_ok=True)
    for ch in scored_channels:
        if ch.channel.contact_email:
            email_data[ch.channel.channel_url] = {
                "email": ch.channel.contact_email,
                "website": ch.channel.website_url,
                "form_url": ch.channel.contact_form_url
            }

    with open("cache/email_data.json", "w", encoding="utf-8") as f:
        json.dump(email_data, f, ensure_ascii=False, indent=2)
    logger.info(f"✅ メール情報保存: {len(email_data)} 件 を JSON に保存")
"""
    new_lines = lines[:insert_pos] + [step7 + '\n'] + lines[insert_pos:]
    
    with open('collect.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print('✅ Step 7 を正しく挿入しました')
else:
    print('❌ # Step 6: CRM 更新 が見つかりません')
