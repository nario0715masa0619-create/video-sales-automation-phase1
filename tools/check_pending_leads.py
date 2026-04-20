from crm_manager import CRMManager
import inspect

crm = CRMManager()

# get_pending_leads のシグネチャを確認
sig = inspect.signature(crm.get_pending_leads)
print(f'get_pending_leads のシグネチャ: {sig}')

# 実際に呼び出す
pending_leads = crm.get_pending_leads()
print(f'取得リード数: {len(pending_leads)}')
print('各リード:')
for i, lead in enumerate(pending_leads[:15], 1):
    ch_name = lead.get('チャンネル名', 'Unknown')
    email = lead.get('メールアドレス', 'N/A')
    print(f'  {i}. {ch_name} ({email})')
