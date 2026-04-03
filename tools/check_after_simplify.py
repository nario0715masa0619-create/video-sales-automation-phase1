with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 終了からStep 6 開始までを表示
for i in range(160, min(195, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
