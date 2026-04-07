with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'dry_run' in line and ('=' in line or 'if' in line):
        print(f'{i+1:4d}: {lines[i].rstrip()}')
