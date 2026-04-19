from db_manager import get_next_email_num

email = 'test_second_email@example.com'
email_num = get_next_email_num(email)

if email_num:
    print(f'✅ メール通数判定: {email_num} 通目')
else:
    print(f'❌ スキップ（4通目以上で送信済み）')
