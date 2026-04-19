from crm_manager import CRMManager

crm = CRMManager()
pending = crm.get_pending_leads()

# テスト企業がいるか確認
test_in_pending = [l for l in pending if 'テスト用2通目' in str(l.get('チャンネル名', ''))]

if test_in_pending:
    print('✅ テスト企業が pending に含まれています')
    for lead in test_in_pending:
        ch_name = lead.get('チャンネル名')
        email = lead.get('メールアドレス')
        print(f'  - {ch_name}: {email}')
else:
    print('❌ テスト企業が pending に含まれていません')
    print(f'pending リード総数: {len(pending)} 件')
    print()
    print('最初の 10 件:')
    for i, lead in enumerate(pending[:10], 1):
        ch_name = lead.get('チャンネル名')
        email = lead.get('メールアドレス')
        print(f'  {i}. {ch_name} ({email})')
