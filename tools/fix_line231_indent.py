with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 231 のインデントを修正
if len(lines) > 230:
    lines[230] = '        sys.exit(1)\n'

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ Line 231 のインデントを修正しました')
