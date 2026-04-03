with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 詳細取得完了の直後のコードを表示
for i, line in enumerate(lines):
    if '詳細取得完了' in line:
        for j in range(i, min(i+15, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
