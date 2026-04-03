print('=== target_scraper.py の構成 ===')
try:
    with open('target_scraper.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f'行数: {len(lines)}')
    for i, line in enumerate(lines[:50]):
        if 'def ' in line or 'import' in line or 'SerpAPI' in line or 'serpapi' in line:
            print(f'{i+1}: {line.strip()}')
except FileNotFoundError:
    print('target_scraper.py が見つかりません')

print()
print('=== email_extractor.py の構成 ===')
try:
    with open('email_extractor.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f'行数: {len(lines)}')
    for i, line in enumerate(lines[:30]):
        if 'def ' in line or 'import' in line:
            print(f'{i+1}: {line.strip()}')
except FileNotFoundError:
    print('email_extractor.py が見つかりません')
