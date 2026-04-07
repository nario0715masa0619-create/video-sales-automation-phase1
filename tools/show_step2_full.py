with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 2 の開始から終了までを表示
in_step2 = False
for i, line in enumerate(lines):
    if 'Step 2' in line and 'チャンネル詳細' in line:
        in_step2 = True
    if in_step2:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
        if '詳細取得完了' in line:
            break
