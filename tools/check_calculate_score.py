with open('scorer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== scorer.py の calculate_score 関数 ===')
for i, line in enumerate(lines):
    if 'def calculate_score' in line:
        for j in range(i, min(i+80, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
