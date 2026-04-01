with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== search_company_channels 関数（行 510 ～ 542）===')
for i in range(509, min(542, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
