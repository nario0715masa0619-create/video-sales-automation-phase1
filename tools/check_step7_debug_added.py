with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 開始から10行を表示
for i, line in enumerate(lines):
    if '=== Step 7: メールアドレス自動取得 ===' in line:
        for j in range(i, min(i+15, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
