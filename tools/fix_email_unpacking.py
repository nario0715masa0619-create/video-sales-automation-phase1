with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 137-139行目を修正
old_code = """        try:
             email = get_email_from_youtube_channel(channel_url)
             ch.contact_email = email if email else ''
             ch.contact_form_url = ''"""

new_code = """        try:
             website_url, email, contact_form_url = get_email_from_youtube_channel(channel_url)
             ch.contact_email = email if email else ''
             ch.website_url = website_url if website_url else ''
             ch.contact_form_url = contact_form_url if contact_form_url else ''"""

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ collect.py を修正しました')
