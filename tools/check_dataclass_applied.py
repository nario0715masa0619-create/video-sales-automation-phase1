with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# @dataclass と class ChannelData を確認
for i, line in enumerate(lines):
    if 'dataclass' in line or 'class ChannelData' in line:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
        if i < len(lines) - 1:
            print(f'{i+2:4d}: {lines[i+1].rstrip()}')
        break
