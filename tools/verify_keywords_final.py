with open('config.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== DEFAULT_SEARCH_KEYWORDS の確認 ===')
for i, line in enumerate(lines):
    if 'DEFAULT_SEARCH_KEYWORDS' in line:
        for j in range(i, min(i+15, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
