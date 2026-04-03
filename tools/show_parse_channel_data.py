with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# parse_channel_data 関数を検索
for i, line in enumerate(lines):
    if 'def parse_channel_data' in line:
        for j in range(i, min(i+50, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
