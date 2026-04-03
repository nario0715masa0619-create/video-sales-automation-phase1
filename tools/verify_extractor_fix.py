with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(135, 145):
    print(f'{i+1:4d}: {lines[i].rstrip()}')
