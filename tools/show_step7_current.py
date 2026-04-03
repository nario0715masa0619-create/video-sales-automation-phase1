with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 のメール取得ループ（136～147行目）を表示
for i in range(135, 148):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
