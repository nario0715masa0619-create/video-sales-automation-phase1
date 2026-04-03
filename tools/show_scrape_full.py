with open('email_extractor.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# scrape_email_from_site 関数全体を表示（167行目から）
for i in range(166, min(280, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
