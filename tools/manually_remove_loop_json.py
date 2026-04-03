with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 192-204行目（JSON 読込・割り当て）を削除
new_lines = []
for i, line in enumerate(lines):
    # 192-204行目をスキップ
    if i >= 191 and i <= 203:
        continue
    new_lines.append(line)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ ループ内の JSON 読込・割り当てコードを削除しました')
