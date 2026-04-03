with open('logs/collect.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# エラーの前後を表示
for i, line in enumerate(lines):
    if '予期しないエラー: name' in line and 'api' in line:
        print('=== エラー周辺 ===')
        for j in range(max(0, i-5), min(i+5, len(lines))):
            print(lines[j].rstrip())
        break
