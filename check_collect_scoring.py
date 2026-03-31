with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# スコアリング と CRM 更新部分を確認
for i, line in enumerate(lines):
    if 'scored_channels = score_channels' in line:
        start = max(0, i - 5)
        end = min(len(lines), i + 30)
        print('=== スコアリング～CRM更新部分 ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
