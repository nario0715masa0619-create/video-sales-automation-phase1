with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== 重複削除後 ===')
for i in range(168, 190):
    if i < len(lines):
        print(f'{i+1:4d}: {lines[i].rstrip()}')
