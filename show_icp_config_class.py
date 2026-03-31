with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ICPConfig クラスを探す
for i, line in enumerate(lines):
    if 'class ICPConfig' in line:
        start = i
        end = min(len(lines), i + 30)
        print('=== ICPConfig クラス ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
