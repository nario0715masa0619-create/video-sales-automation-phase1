with open('scorer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# score_channels 関数を探す
for i, line in enumerate(lines):
    if 'def score_channels' in line:
        start = i
        end = min(len(lines), i + 50)
        print('=== score_channels 関数 ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
