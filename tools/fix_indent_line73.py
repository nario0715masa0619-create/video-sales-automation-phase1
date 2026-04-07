with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 73 のインデントを修正
for i in range(len(lines)):
    if i == 72 and 'return' in lines[i]:
        # インデントを 8 スペースに修正
        lines[i] = '        return\n'
        break

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ Line 73 のインデントを修正しました')
