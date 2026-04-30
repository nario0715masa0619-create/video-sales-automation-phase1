import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('website_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 40～120 行を表示（scrape_website 関数）
for i in range(39, min(120, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
