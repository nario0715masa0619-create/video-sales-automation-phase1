with open('website_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(119, min(145, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
