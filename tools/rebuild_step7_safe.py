import re

with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 7 セクションを見つけて置換
pattern = r'(logger\.info\("\n=== Step 7: メールアドレス自動取得 ==="\)).*?(# Step 6: CRM 更新)'
replacement = r'''\1
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

    \2'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 7 を再構築しました')
