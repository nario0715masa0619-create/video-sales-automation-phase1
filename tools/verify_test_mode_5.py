with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'scored_channels = scored_channels[:5]' in content:
    print('✅ テストモード有効: 5件')
else:
    print('❌ テストモード無効')
