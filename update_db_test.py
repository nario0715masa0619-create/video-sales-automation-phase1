import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('logs/send_log.db')
c = conn.cursor()

# テスト用2回目送信対象を削除（前回のテスト用レコード）
c.execute('DELETE FROM send_log WHERE to_address = ?', ('test_second_email@example.com',))

# 3日以上前に送信されたレコードを作成（2通目対象にする）
test_email = 'test_second_email@example.com'
past_date = (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d %H:%M:%S')

c.execute('INSERT INTO send_log (datetime, from_address, to_address, message_id, campaign_id, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
    (past_date, 'marketing@luvira-biz.jp', test_email, 'test_msg_001', 'campaign_001', 'sent', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

conn.commit()
conn.close()

print(f'✅ テスト企業の送信履歴を更新しました')
print(f'  - 送信日: {past_date}')
print(f'  - メール: {test_email}')
print(f'  - 次の送信: 2通目対象')
