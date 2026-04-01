from crm_manager import CRMManager
crm = CRMManager()
leads = crm.get_all_leads()

print('=== メールアドレス保有リード（全て）===')
email_leads = [lead for lead in leads if lead.get('メールアドレス')]
for i, lead in enumerate(email_leads, 1):
    ch_name = lead.get('チャンネル名', '')
    rank = lead.get('ランク', '')
    email = lead.get('メールアドレス', '')
    status = lead.get('送信ステータス', '')
    print(f'{i}. {ch_name:30} | ランク: {rank:1} | ステータス: {status:10} | {email}')

print(f'\n合計: {len(email_leads)} 件')
