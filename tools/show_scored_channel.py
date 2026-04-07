with open('scorer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ScoredChannel クラスを探す
for i, line in enumerate(lines):
    if 'class ScoredChannel' in line:
        for j in range(i, min(i+20, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
