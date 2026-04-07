with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# score_channels 関数を探す
for i, line in enumerate(lines):
    if 'def score_channels' in line or 'from' in line and 'score_channels' in line:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
