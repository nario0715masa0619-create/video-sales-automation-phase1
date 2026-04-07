with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# キーワード定義を探す
for i, line in enumerate(lines):
    if 'キーワード' in line or 'KEYWORD' in line or 'YouTube 集客' in line:
        print(f'{i+1}: {line.rstrip()}')
