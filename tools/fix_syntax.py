with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 155行目の不正な部分を削除（直後に挿入したデバッグコード）
# 154行目の正しい行まで保持し、その後の不正な部分を削除
lines = content.split('\n')

# 153行目（0-indexed）まで保持
correct_lines = lines[:154]

# その後、Step 6 以降の内容を探す
for i, line in enumerate(lines):
    if 'Step 6' in line:
        correct_lines.extend(lines[i:])
        break

content = '\n'.join(correct_lines)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ collect.py を修復しました')
