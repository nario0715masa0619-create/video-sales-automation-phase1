with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修正 1: Step 7 で ch.contact_email → ch.channel.contact_email
content = content.replace(
    'ch.contact_email = email if email else',
    'ch.channel.contact_email = email if email else'
)
content = content.replace(
    'ch.website_url = website_url if website_url else',
    'ch.channel.website_url = website_url if website_url else'
)
content = content.replace(
    'ch.contact_form_url = contact_form_url if contact_form_url else',
    'ch.channel.contact_form_url = contact_form_url if contact_form_url else'
)

# 修正 2: Step 7 の JSON 保存コードを追加（Step 7 完了ログの後）
old_step7_end = '''    logger.info(f"✅ Step 7 完了: {email_count} 件のメール取得")

    # Step 6: CRM 更新'''

new_step7_end = '''    logger.info(f"✅ Step 7 完了: {email_count} 件のメール取得")

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

content = content.replace(old_step7_end, new_step7_end)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 7 を修正しました')
