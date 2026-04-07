with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 のメール取得ループを表示
for i in range(127, 150):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
