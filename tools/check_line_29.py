with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 27-32行目を表示
for i in range(26, min(32, len(lines))):
    print(f'{i+1:4d}: {repr(lines[i])}')
