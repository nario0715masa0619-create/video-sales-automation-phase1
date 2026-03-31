with open('logs/collect.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 最初と最後のログの日時を抽出
if lines:
    first_date = lines[0].split('|')[0].strip()
    last_date = lines[-1].split('|')[0].strip()
    print(f'ログの日時範囲:')
    print(f'  最初: {first_date}')
    print(f'  最後: {last_date}')
    print(f'  総ログ行数: {len(lines)}')

# 日付ごとのログ数を集計
from collections import Counter
dates = [line.split('|')[0].split()[0] for line in lines if '|' in line]
date_counts = Counter(dates)

print(f'\n日付ごとのログ行数:')
for date in sorted(date_counts.keys()):
    print(f'  {date}: {date_counts[date]}行')
