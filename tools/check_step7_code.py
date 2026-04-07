with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 のメール抽出部分を表示（130～160行目）
for i in range(129, min(160, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
