with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 終了からStep 6 開始までの間に scored_channels がどう使われているか確認
print('=== Step 7 終了～Step 6 開始の間 ===')
for i, line in enumerate(lines):
    if 'Step 7 完了' in line:
        # Step 7 終了からStep 6 開始までを表示
        for j in range(i, min(i+20, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
