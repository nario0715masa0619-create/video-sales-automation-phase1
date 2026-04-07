with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 ループ開始部分を確認（185～210行目）
for i in range(184, min(210, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
