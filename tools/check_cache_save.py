with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# キャッシュ保存部分を探す
for i, line in enumerate(lines):
    if 'cache' in line.lower() and ('save' in line.lower() or 'dump' in line.lower()):
        print(f'{i+1:4d}: {line.rstrip()}')
