with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 の CRM 更新ループを表示
for i in range(155, min(175, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
