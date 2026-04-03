from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

print('=== メールアドレス保有リード（全A/B ランク）===')
ab_leads = [lead for lead in leads if lead.get('メールアドレス') and lead.get('ランク') in ['A', 'B']]

for lead in ab_leads:
    ch_name = lead.get('チャンネル名', '')
    rank = lead.get('ランク', '')
    status = lead.get('営業ステータス', '')
    send_count = lead.get('メール送信回数', '')
    send_date = lead.get('1通目送信日', '')
    print(f'{ch_name:30} | ランク: {rank} | ステータス: {status:10} | 送信回数: {send_count} | 送信日: {send_date}')
