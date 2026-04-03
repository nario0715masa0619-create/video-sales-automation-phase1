with open('email_extractor.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# get_website_from_youtube 関数を検索
for i, line in enumerate(lines):
    if 'def get_website_from_youtube' in line:
        print('=== get_website_from_youtube ===')
        for j in range(i, min(i+30, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        print()
        break

# scrape_email_from_site 関数を検索
for i, line in enumerate(lines):
    if 'def scrape_email_from_site' in line:
        print('=== scrape_email_from_site ===')
        for j in range(i, min(i+40, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
