with open('email_extractor.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# _get_website_via_ytdlp と _get_website_via_html を検索
for i, line in enumerate(lines):
    if 'def _get_website_via_ytdlp' in line or 'def _get_website_via_html' in line:
        print(f'\n=== {line.strip()} ===')
        for j in range(i, min(i+25, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
