with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 ループ部分を表示
for i, line in enumerate(lines):
    if 'Step 6' in line and 'CRM' in line:
        for j in range(i, min(i+25, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
