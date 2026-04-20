import sqlite3
from datetime import date

conn = sqlite3.connect('logs/send_log.db')
cur = conn.cursor()

today = date.today().isoformat()
print(f'今日の日付: {today}')
print(f'\n=== send_log から本日送信を検索 ===')

cur.execute('''
    SELECT COUNT(*), DATE(datetime) 
    FROM send_log 
    GROUP BY DATE(datetime)
    ORDER BY DATE(datetime) DESC
    LIMIT 10
''')

for count, date_str in cur.fetchall():
    print(f'{date_str}: {count}件')

print(f'\n=== 本日（{today}）のメール詳細 ===')
cur.execute('''
    SELECT datetime, to_address, status 
    FROM send_log 
    WHERE DATE(datetime) = ?
    ORDER BY datetime
''', (today,))

results = cur.fetchall()
print(f'本日送信件数: {len(results)}件\n')
for dt, email, status in results:
    print(f'{dt}: {email} ({status})')

conn.close()
