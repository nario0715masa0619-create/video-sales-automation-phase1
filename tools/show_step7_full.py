with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 ループの最初と最後を表示
print('=== Step 7 ループ部分 ===')
for i, line in enumerate(lines):
    if '=== Step 7: メールアドレス自動取得 ===' in line:
        # Step 7 開始から Step 8 または キャッシュ保存まで表示
        for j in range(i, min(i+50, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
            if 'キャッシュ保存' in lines[j]:
                break
        break
