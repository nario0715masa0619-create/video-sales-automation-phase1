with open('config.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'DEFAULT_SEARCH_KEYWORDS' in line:
        print(f'=== 行 {i+1} から ===')
        for j in range(i, min(i+15, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
