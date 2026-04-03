with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 ループの部分を表示（200～225行目）
print('=== Step 6 ループ部分 ===')
for i in range(199, min(225, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
