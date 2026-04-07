print('=== target_scraper.py 内の SerpAPI 関連 ===')
with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

serpapi_lines = []
for i, line in enumerate(lines):
    if 'serpapi' in line.lower() or 'SerpAPI' in line or 'api_key' in line.lower():
        serpapi_lines.append((i+1, line.strip()))

print(f'見つかった行数: {len(serpapi_lines)}')
for line_num, content in serpapi_lines[:20]:
    print(f'{line_num}: {content[:100]}')

# 関数定義を確認
print()
print('=== target_scraper.py の関数一覧 ===')
for i, line in enumerate(lines):
    if line.startswith('def '):
        print(f'{i+1}: {line.strip()}')
