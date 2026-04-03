with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'✅ 復元完了: 全 {len(lines)} 行')

# Step 7 を確認
for i, line in enumerate(lines):
    if '=== Step 7' in line:
        for j in range(i, min(i+5, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
