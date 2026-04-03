with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# APIキー関連の行を検索
for i, line in enumerate(lines):
    if 'YOUTUBE_API_KEY' in line or 'API_KEY' in line or 'api_key' in line.lower():
        print(f'{i+1:4d}: {line.rstrip()}')
