with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 2+3 のセクション（大体 70-85 行目）を表示
print('=== Step 2+3 セクション ===')
for i in range(69, min(90, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
