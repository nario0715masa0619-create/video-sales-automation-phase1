with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# pickle を参照している行をすべて削除
filtered_lines = []
for line in lines:
    if 'scored_channels.pkl' not in line and 'import pickle' not in line:
        filtered_lines.append(line)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(filtered_lines)

print('✅ pickle 参照をすべて削除しました')
