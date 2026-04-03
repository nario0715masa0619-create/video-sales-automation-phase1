with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ChannelData クラスを探して @dataclass を追加
for i, line in enumerate(lines):
    if 'class ChannelData' in line:
        # その前の行に @dataclass があるか確認
        if i > 0 and '@dataclass' not in lines[i-1]:
            # @dataclass を追加
            lines.insert(i, '@dataclass\n')
            print(f'✅ @dataclass を {i+1} 行目に追加しました')
        break

with open('target_scraper.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ target_scraper.py を修正しました')
