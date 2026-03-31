from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

# チャンネルURL の一覧を表示
print(f'現在登録されているチャンネルURL数: {len(leads)}')
print('\n最初の 10 件のチャンネル:')
for i, lead in enumerate(leads[:10], 1):
    print(f'{i}. {lead.get("チャンネル名")}: {lead.get("チャンネルURL")}')

# スコアが低いチャンネルも確認
print('\nC-rank（低スコア）のチャンネル:')
c_rank_leads = [l for l in leads if l.get('ランク') == 'C']
for i, lead in enumerate(c_rank_leads[:10], 1):
    score = lead.get('総合スコア', 'N/A')
    print(f'{i}. {lead.get("チャンネル名")} - スコア: {score}')
