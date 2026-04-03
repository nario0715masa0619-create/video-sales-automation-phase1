with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 ループ開始部分を確認（206～225行目）
for i in range(205, min(225, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
