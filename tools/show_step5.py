with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 5 を探す
for i, line in enumerate(lines):
    if 'Step 5' in line and 'スコア' in line:
        for j in range(i, min(i+10, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
