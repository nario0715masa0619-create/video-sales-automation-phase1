with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'キャッシュ保存' in line or 'pickle.dump' in line:
        # 前後5行も表示
        start = max(0, i-2)
        end = min(len(lines), i+3)
        for j in range(start, end):
            prefix = '>>>' if j == i else '   '
            print(f'{j+1:4d} {prefix} {lines[j].rstrip()}')
        print()
