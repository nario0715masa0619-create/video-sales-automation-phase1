with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Step 7 確認 ===')
for i, line in enumerate(lines):
    if '=== Step 7' in line:
        for j in range(i, min(i+50, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
