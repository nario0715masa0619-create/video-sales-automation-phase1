with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# youtube_api の定義を探す
for i, line in enumerate(lines):
    if 'youtube_api' in line and '=' in line:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
