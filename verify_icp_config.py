with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ICPConfig クラスを表示
in_class = False
for i, line in enumerate(lines, 1):
    if 'class ICPConfig' in line:
        in_class = True
    if in_class:
        print(f'{i}: {line.rstrip()}')
        if line.strip() == '' and i > 60:
            break
