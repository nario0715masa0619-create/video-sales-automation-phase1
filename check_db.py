import sqlite3

conn = sqlite3.connect('logs/phase5_data.db')
cursor = conn.cursor()

# テーブル一覧取得
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print('【DB に存在するテーブル】')
for table in tables:
    print(f'  - {table[0]}')
    
    # 各テーブルのカラム確認
    cursor.execute(f'PRAGMA table_info({table[0]})')
    columns = cursor.fetchall()
    print(f'    カラム数: {len(columns)}')
    for col in columns:
        print(f'      - {col[1]} ({col[2]})')

conn.close()
