with open('scorer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# score_channels 関数を表示
for i, line in enumerate(lines):
    if 'def score_channels' in line:
        for j in range(i, min(i+15, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
