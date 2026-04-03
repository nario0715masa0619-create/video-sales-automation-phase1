with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1件から2件に変更
content = content.replace('scored_channels[:1]', 'scored_channels[:2]')

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ テストモードを2件に変更しました')
