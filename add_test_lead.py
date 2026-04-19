from crm_manager import CRMManager

crm = CRMManager()

# テスト企業を追加（チャンネルURL を追加）
test_lead = {
    'チャンネル名': 'テスト用2通目送信企業',
    'チャンネルURL': 'https://www.youtube.com/c/testsecond',
    'メールアドレス': 'test_second_email@example.com',
    'サイトURL': 'https://example.com',
    '登録ステータス': 'ペンディング',
    'ランク': 'A',
    'NG企業': False,
}

result = crm.upsert_lead(test_lead)
print('✅ テスト企業をCRMに追加しました')
ch_name = test_lead['チャンネル名']
email = test_lead['メールアドレス']
print(f'チャンネル名: {ch_name}')
print(f'メール: {email}')
