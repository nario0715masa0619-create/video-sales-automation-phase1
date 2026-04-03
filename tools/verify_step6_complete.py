with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Step 6 修正後 ===')
for i in range(148, 170):
    if i < len(lines):
        print(f'{i+1:4d}: {lines[i].rstrip()}')
