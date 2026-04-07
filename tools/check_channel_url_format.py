with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# チャンネルURL取得部分を探す
for i, line in enumerate(lines):
    if 'channel_url = ch.channel_url' in line:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
        break

# 代わりに、parse_channel_data でどうチャンネルURL生成されているか確認
with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'channel_url' in line and ('https://' in line or 'youtube.com' in line):
        print(f'target_scraper.py {i+1:4d}: {lines[i].rstrip()}')
