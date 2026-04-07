with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修正 1: extractor.extract_email → get_email_from_youtube_channel
content = content.replace(
    'website_url, email, contact_form_url = extractor.extract_email(channel_url)',
    'website_url, email, contact_form_url = get_email_from_youtube_channel(channel_url)'
)

# 修正 2: ch.website_url の割り当てを復元
content = content.replace(
    '''            ch.channel.contact_email = email if email else ''
            ch.channel.contact_form_url = contact_form_url if contact_form_url else \'\'\'',
    '''            ch.channel.contact_email = email if email else ''
            ch.channel.website_url = website_url if website_url else ''
            ch.channel.contact_form_url = contact_form_url if contact_form_url else \'\'\'
)

# 修正 3: JSON 保存コードを追加
old_end = '''    logger.info(f"✅ Step 7 完了: {email_count} 件のメール取得")


    # Step 6: CRM 更新'''

new_end = '''    logger.info(f"✅ Step 7 完了: {email_count} 件のメール取得")

    # JSON にメール情報を保存
    os.makedirs("cache", exist_ok=True)
    email_data = {}
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

    # Step 6: CRM 更新'''

content = content.replace(old_end, new_end)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 7 を完全修正しました')
