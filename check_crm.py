from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()
print(f'スプシ内の総リード数: {len(leads)}')

# ランク別集計
a_rank = [l for l in leads if l.get('営業ランク') == 'A']
b_rank = [l for l in leads if l.get('営業ランク') == 'B']
c_rank = [l for l in leads if l.get('営業ランク') == 'C']

print(f'A-rank: {len(a_rank)}')
print(f'B-rank: {len(b_rank)}')
print(f'C-rank: {len(c_rank)}')

# 最新の10件を表示
print('\n最新10件:')
for i, lead in enumerate(leads[-10:], 1):
    ch_name = lead.get('チャンネル名', 'N/A')
    rank = lead.get('営業ランク', '未設定')
    print(f'{i}. {ch_name} - {rank}')
