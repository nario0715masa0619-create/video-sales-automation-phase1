from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

# テストチャンネルを探す
for lead in leads:
    if 'テストチャンネル' in lead.get('チャンネル名', ''):
        print('=== テストチャンネルのデータ ===')
        ch_name = lead.get('チャンネル名')
        company = lead.get('会社名')
        rank = lead.get('ランク')
        email = lead.get('メールアドレス')
        print(f'チャンネル名: {repr(ch_name)}')
        print(f'会社名: {repr(company)}')
        print(f'ランク: {repr(rank)}')
        print(f'メールアドレス: {repr(email)}')
        break
