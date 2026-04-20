from crm_manager import get_crm
crm = get_crm()
leads = crm.get_all_leads()

total = len(leads)
with_email = sum(1 for l in leads if l.get('メールアドレス'))

print(f'CRM 統計:')
print(f'  総リード: {total} 件')
print(f'  メール情報: {with_email} 件')
print(f'  成功率: {with_email/total*100:.1f}%')
print(f'\n最新10件のメール:')
for lead in leads[-10:]:
    email = lead.get('メールアドレス', '未取得')
    name = lead.get('チャンネル名', 'N/A')
    print(f'  {name[:30]:30} → {email}')
