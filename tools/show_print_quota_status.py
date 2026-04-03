with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# print_quota_status 関数を表示
for i, line in enumerate(lines):
    if 'def print_quota_status' in line:
        for j in range(i, min(i+10, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
