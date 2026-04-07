with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 終了～Step 6 開始までの全コードを表示
print('=== Step 7 終了～Step 6 開始 ===')
for i, line in enumerate(lines):
    if 'logger.info(f"✅ Step 7 完了' in line:
        for j in range(i, min(i+25, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
