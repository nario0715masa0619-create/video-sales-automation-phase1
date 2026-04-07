with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 重複するメール割り当てコードを削除
new_lines = []
skip_until = -1
for i, line in enumerate(lines):
    if i < skip_until:
        continue
    
    # 176-180 行の重複を検出して削除
    if i == 175 and '# JSON からメール情報を割り当て' in line:
        # 次の 5 行をスキップ（176-180）
        skip_until = i + 6
        continue
    
    new_lines.append(line)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ 重複するメール割り当てコードを削除しました')
