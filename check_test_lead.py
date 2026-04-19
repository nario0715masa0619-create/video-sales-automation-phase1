from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

# test_second_email を検索
test_leads = [l for l in leads if 'test_second_email' in str(l.get('メールアドレス', ''))]

if test_leads:
    print(f'✅ テスト企業が見つかりました: {len(test_leads)} 件')
    for lead in test_leads:
        ch_name = lead.get('チャンネル名')
        email = lead.get('メールアドレス')
        print(f'  - {ch_name}: {email}')
else:
    print('❌ テスト企業が見つかりません')
    print(f'全リード数: {len(leads)} 件')
