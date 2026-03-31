with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# filter_by_icp 関数を探す
for i, line in enumerate(lines):
    if 'def filter_by_icp' in line:
        start = i
        end = min(len(lines), i + 50)
        print('=== filter_by_icp 関数 ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
