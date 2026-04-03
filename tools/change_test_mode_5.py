with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# テストモードを 2件 → 5件に変更
content = content.replace(
    'scored_channels = scored_channels[:1]',
    'scored_channels = scored_channels[:5]'
)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ テストモードを 5件に変更しました')
