from crm_manager import CRMManager
from utils import normalize_url

crm = CRMManager()
leads = crm.get_all_leads()

# 問い合わせフォームURL を正規化
fixed_count = 0
for lead in leads:
    if lead.get('問い合わせフォームURL'):
        original = lead['問い合わせフォームURL']
        normalized = normalize_url(original)
        if original != normalized:
            lead['問い合わせフォームURL'] = normalized
            fixed_count += 1
            print(f"修正: {lead.get('チャンネル名')}")
            print(f"  Before: {original}")
            print(f"  After:  {normalized}")
            crm.upsert_lead(lead)

print(f'\n✅ {fixed_count}件のURLを修正しました')
