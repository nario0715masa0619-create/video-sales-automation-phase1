with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# メール設定直後のデバッグを強化
old_code = '''            website_url, email, contact_form_url = get_email_from_youtube_channel(channel_url)
            ch.contact_email = email if email else ''
            ch.website_url = website_url if website_url else ''
            ch.contact_form_url = contact_form_url if contact_form_url else ''
            if email:'''

new_code = '''            website_url, email, contact_form_url = get_email_from_youtube_channel(channel_url)
            ch.contact_email = email if email else ''
            ch.website_url = website_url if website_url else ''
            ch.contact_form_url = contact_form_url if contact_form_url else ''
            # 即座に確認
            logger.debug(f"ASSIGN直後: {company_name} → email='{ch.contact_email}' (from func: '{email}')")
            if email:'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ メール割り当て直後のデバッグを強化しました')
