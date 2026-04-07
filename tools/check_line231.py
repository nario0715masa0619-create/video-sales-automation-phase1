with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Line 228-235 確認 ===')
for i in range(227, 235):
    if i < len(lines):
        print(f'{i+1:4d}: {repr(lines[i])}')
