from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()
print(f'✅ スプレッドシート読み込み成功: {len(leads)} 件')

# Step 2: 新規リード追加テスト
test_lead = {
    'チャンネル名': 'テストチャンネル',
    'チャンネルURL': 'https://www.youtube.com/@test123/videos',
    'ランク': 'B',
    'メールアドレス': 'test@example.com'
}
crm.upsert_lead(test_lead)
print('✅ テストリード追加完了')

# Step 3: 追加確認
leads_after = crm.get_all_leads()
print(f'✅ スプレッドシート更新確認: {len(leads_after)} 件')
