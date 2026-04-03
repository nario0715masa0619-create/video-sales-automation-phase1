with open('email_extractor.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# scrape_email_from_site 関数の続き（280行目以降）
for i in range(279, min(362, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
