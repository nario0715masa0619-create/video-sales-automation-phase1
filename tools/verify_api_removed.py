with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'current_quota_usage = api' in content:
    print('❌ まだクォータチェックが残っています')
else:
    print('✅ クォータチェック削除完了')
