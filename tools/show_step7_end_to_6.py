with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 完了からStep 6 開始まで
in_step7_end = False
for i, line in enumerate(lines):
    if '✅ Step 7 完了' in line:
        in_step7_end = True
    if in_step7_end:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
        if 'Step 6: CRM' in line:
            break
