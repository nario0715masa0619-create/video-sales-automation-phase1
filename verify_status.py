from crm_manager import CRMManager, LEADS_COLUMNS

crm = CRMManager()
leads = crm.get_all_leads()

print('=== メールアドレス保有リード（送信ステータス確認）===')
email_leads = [lead for lead in leads if lead.get('メールアドレス')]
for lead in email_leads[:4]:
    ch_name = lead.get('チャンネル名', '')
    status = lead.get('送信ステータス', '')
    email = lead.get('メールアドレス', '')
    print(f'{ch_name:30} | ステータス: {status:10} | {email}')
