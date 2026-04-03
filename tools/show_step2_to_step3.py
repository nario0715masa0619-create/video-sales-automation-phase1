with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 2 完了後からStep 3 までを表示
print('=== Step 2 完了～Step 3 開始 ===')
for i, line in enumerate(lines):
    if '詳細取得完了:' in line:
        for j in range(i, min(i+15, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
