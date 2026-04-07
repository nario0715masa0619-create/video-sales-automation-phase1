with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# extractor.extract_email() を get_email_from_youtube_channel() に変更
old_code = '''            website_url, email, contact_form_url = extractor.extract_email(channel_url)'''

new_code = '''            website_url, email, contact_form_url = get_email_from_youtube_channel(channel_url)'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ extractor.extract_email() を get_email_from_youtube_channel() に変更しました')
