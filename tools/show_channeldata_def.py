with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ChannelData クラス定義を表示
for i, line in enumerate(lines):
    if 'class ChannelData' in line:
        for j in range(i, min(i+40, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
