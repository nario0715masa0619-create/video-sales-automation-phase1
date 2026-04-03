with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 の最初に json import を追加
for i, line in enumerate(lines):
    if '=== Step 7: メールアドレス自動取得 ===' in line:
        insert_pos = i + 1
        lines.insert(insert_pos, '    import json\n')
        break

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('OK')
