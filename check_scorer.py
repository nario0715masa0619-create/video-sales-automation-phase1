with open('scorer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== scorer.py の score_channels 関数（最初の 50 行）===')
for i, line in enumerate(lines):
    if 'def score_channels' in line:
        for j in range(i, min(i+50, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
