with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 7 でのメール割り当てを修正
old_code = '''            website_url, email, contact_form_url = get_email_from_youtube_channel(channel_url)
            ch.contact_email = email if email else ''
            ch.website_url = website_url if website_url else ''
            ch.contact_form_url = contact_form_url if contact_form_url else ''''

new_code = '''            website_url, email, contact_form_url = get_email_from_youtube_channel(channel_url)
            ch.channel.contact_email = email if email else ''
            ch.channel.website_url = website_url if website_url else ''
            ch.channel.contact_form_url = contact_form_url if contact_form_url else ''''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 7 のメール割り当てを修正しました (ch.contact_email → ch.channel.contact_email)')
