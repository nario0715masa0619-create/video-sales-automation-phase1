with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Step 6 確認 ===')
for i, line in enumerate(lines):
    if '=== Step 6: CRM 更新 ===' in line:
        for j in range(i, min(i+30, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
