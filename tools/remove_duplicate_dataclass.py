with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 重複した @dataclass を削除
new_lines = []
skip_next_dataclass = False
for i, line in enumerate(lines):
    if '@dataclass' in line:
        if skip_next_dataclass:
            continue
        skip_next_dataclass = True
    else:
        skip_next_dataclass = False
    new_lines.append(line)

with open('target_scraper.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ 重複した @dataclass を削除しました')
