with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'scored_channels = scored_channels[:1]' in content:
    print('✅ テストモードが有効です')
else:
    print('❌ テストモードが有効化されていません')
