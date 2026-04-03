with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'scored_channels = scored_channels[:' in content:
    print('✅ テストモードが有効です')
    # どの数字になっているか確認
    import re
    match = re.search(r'scored_channels = scored_channels\[:(\d+)\]', content)
    if match:
        print(f'   処理件数: {match.group(1)} 件')
else:
    print('❌ テストモードが無効です')
