import sqlite3

conn = sqlite3.connect('logs/phase5_data.db')
cursor = conn.cursor()

# 総レコード数
cursor.execute('SELECT COUNT(*) FROM phase5_data')
total = cursor.fetchone()[0]
print(f'【総レコード数】{total}')

# 最新10件
print('\n【最新10件のデータ】')
cursor.execute('''
    SELECT company_name, phone_number, email, status, scraped_at 
    FROM phase5_data 
    ORDER BY scraped_at DESC 
    LIMIT 10
''')

for row in cursor.fetchall():
    print(f'{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}')

conn.close()
