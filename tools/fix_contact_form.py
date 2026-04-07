with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "ch.contact_form_url = ''",
    "ch.contact_form_url = email if email else ''"
)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ contact_form_url を修正しました')
