with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== 重複排除ロジック確認 ===')
for i in range(71, min(85, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
