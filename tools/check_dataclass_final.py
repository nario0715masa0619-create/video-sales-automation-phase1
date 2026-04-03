with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '@dataclass' in line or 'class ChannelData' in line:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
