with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# api を youtube_api に置換
content = content.replace('api.quota_used', 'youtube_api.quota_used')
content = content.replace('api = ', 'youtube_api = ')

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ api を youtube_api に変更しました')
