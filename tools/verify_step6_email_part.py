with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Step 6 メール割り当て部分 ===')
for i in range(168, 185):
    if i < len(lines):
        print(f'{i+1:4d}: {lines[i].rstrip()}')
