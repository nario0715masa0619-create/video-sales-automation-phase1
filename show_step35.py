with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 3.5 付近（85行目から 120行目）を確認
print('=== Step 3.5 付近のコード ===')
for i in range(84, min(120, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
