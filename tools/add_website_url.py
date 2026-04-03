with open('target_scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# website_url 属性を追加（contact_email の前に）
old_line = '    contact_email: str = ""'
new_lines = '''    website_url: str = ""
    contact_email: str = ""'''

content = content.replace(old_line, new_lines)

with open('target_scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ website_url 属性を ChannelData に追加しました')
