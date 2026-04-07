with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 'api' が含まれる行を全て表示
print('=== api を含む行 ===')
for i, line in enumerate(lines):
    if 'api' in line.lower() and 'youtube_api' not in line and 'api_key' not in line:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
