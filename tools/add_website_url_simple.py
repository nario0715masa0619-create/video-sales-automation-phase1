with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 139行目を追加
old_code = '''            ch.contact_email = email if email else ''
            ch.contact_form_url = contact_form_url if contact_form_url else ''
            if email:'''

new_code = '''            ch.contact_email = email if email else ''
            ch.website_url = website_url if website_url else ''
            ch.contact_form_url = contact_form_url if contact_form_url else ''
            if email:'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ website_url 割り当てを追加しました')
