with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'print_quota_status()' in content:
    print('❌ まだ print_quota_status() が残っています')
else:
    print('✅ print_quota_status() の呼び出しを削除完了')
