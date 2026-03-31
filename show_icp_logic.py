with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ICP フィルタリング条件を表示
print('=== ICP フィルタリング条件 ===')
for i, line in enumerate(lines):
    if 'icp_filter' in line.lower() or 'passed_channels' in line or 'ICP_' in line:
        start = max(0, i - 2)
        end = min(len(lines), i + 10)
        for j in range(start, end):
            print(f'{j+1}: {lines[j].rstrip()}')
        print('---')
        break
