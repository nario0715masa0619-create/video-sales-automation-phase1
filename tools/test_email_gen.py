from email_generator import generate_email

lead_dict = {
    'チャンネル名': 'テスト用2通目送信企業',
    'メールアドレス': 'test_second_email@example.com',
    'サイトURL': 'https://example.com',
}

# 2通目を生成
try:
    result = generate_email(lead_dict, email_num=2)
    print('✅ 2通目メール生成成功')
    print(f'件名: {result.subject}')
    print(f'本文（先頭200字）: {result.body[:200]}')
except Exception as e:
    print(f'❌ エラー: {e}')
