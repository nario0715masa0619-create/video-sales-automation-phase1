with open('website_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_function = False
for i, line in enumerate(lines, 1):
    if 'def scrape_website' in line:
        in_function = True
    if in_function:
        print(f'{i}: {line.rstrip()}')
        if i > 100 and 'return' in line:
            break
