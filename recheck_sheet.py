from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

print(f'現在のシート内リード数: {len(leads)}')

# ランク別に集計
a_rank = len([l for l in leads if l.get('ランク') == 'A'])
b_rank = len([l for l in leads if l.get('ランク') == 'B'])
c_rank = len([l for l in leads if l.get('ランク') == 'C'])

print(f'A-rank: {a_rank}')
print(f'B-rank: {b_rank}')
print(f'C-rank: {c_rank}')
