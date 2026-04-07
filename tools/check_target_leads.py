from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

print('=== A/B ランク + 営業ステータス=未接触のリード ===')
target_leads = [
    lead for lead in leads
    if lead.get('メールアドレス')
    and lead.get('ランク') in ['A', 'B']
    and lead.get('営業ステータス') == '未接触'
]

print(f'合計: {len(target_leads)} 件')
for lead in target_leads[:10]:
    ch_name = lead.get('チャンネル名', '')
    rank = lead.get('ランク', '')
    status = lead.get('営業ステータス', '')
    email = lead.get('メールアドレス', '')
    print(f'{ch_name:30} | ランク: {rank} | ステータス: {status:10} | {email}')
