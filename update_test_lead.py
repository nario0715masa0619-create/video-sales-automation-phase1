from crm_manager import CRMManager

crm = CRMManager()

# テスト企業を更新：メール送信回数を明示的に 0 に設定
test_lead = {
    'チャンネル名': 'テスト用2通目送信企業',
    'チャンネルURL': 'https://www.youtube.com/c/testsecond',
    'メールアドレス': 'test_second_email@example.com',
    'サイトURL': 'https://example.com',
    '登録ステータス': 'ペンディング',
    'ランク': 'A',
    'NG企業': False,
    'メール送信回数': 0,
}

result = crm.upsert_lead(test_lead)
print('✅ テスト企業を更新しました（メール送信回数: 0）')
