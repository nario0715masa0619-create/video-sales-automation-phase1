with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 直前のコードを表示（170～195行目）
print('=== Step 6 直前のコード ===')
for i in range(169, min(195, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
