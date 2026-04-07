with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# テストモードを無効化
content = content.replace(
    'scored_channels = scored_channels[:5]',
    '# テストモード無効化\n    # scored_channels = scored_channels[:5]'
)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ テストモードを無効化しました')
