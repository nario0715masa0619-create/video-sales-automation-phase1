with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 過剰なインデントを持つ return 文を全て修正
for i in range(len(lines)):
    if 'return' in lines[i]:
        stripped = lines[i].lstrip()
        if stripped == 'return\n':
            # インデントを 8 スペースに統一
            lines[i] = '        return\n'

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ 全ての return 文のインデントを修正しました')
