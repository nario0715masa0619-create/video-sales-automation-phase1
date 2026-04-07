with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'extractor' in line and ('=' in line or 'import' in line):
        print(f'{i+1:4d}: {lines[i].rstrip()}')
