with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Step 2+3 セクション ===')
for i in range(69, min(95, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
