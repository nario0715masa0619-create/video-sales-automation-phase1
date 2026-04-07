with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'scored_channels = scored_channels[:' in content:
    import re
    match = re.search(r'scored_channels = scored_channels\[:\d+\]', content)
    if match:
        print(f'✅ テストモード: {match.group()}')
else:
    print('❌ テストモード無効（全件処理）')
