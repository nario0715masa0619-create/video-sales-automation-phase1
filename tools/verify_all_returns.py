with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== return 文の確認 ===')
for i, line in enumerate(lines):
    if 'return' in line:
        print(f'{i+1:4d}: {repr(line)}')
