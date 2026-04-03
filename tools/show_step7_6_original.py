with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 完了からStep 6 開始までを表示
in_step7 = False
for i, line in enumerate(lines):
    if 'Step 7' in line and 'メール' in line:
        in_step7 = True
    if in_step7:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
        if 'Step 6' in line and 'CRM' in line:
            for j in range(i+1, min(i+20, len(lines))):
                print(f'{j+1:4d}: {lines[j].rstrip()}')
            break
