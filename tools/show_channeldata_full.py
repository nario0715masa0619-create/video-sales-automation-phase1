with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ChannelData クラス定義（16～50行目）
for i in range(15, min(50, len(lines))):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
