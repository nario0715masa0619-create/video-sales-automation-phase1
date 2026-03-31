with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 1 の全体を確認
for i, line in enumerate(lines):
    if 'Step 1:' in line:
        start = i
        end = min(len(lines), i + 50)
        print('=== Step 1: スクレイピング ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
