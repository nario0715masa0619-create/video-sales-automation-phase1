from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

# ゴミ文字付きURLを検索
dirty_urls = [l for l in leads if l.get('問い合わせフォームURL') and any(c in l['問い合わせフォームURL'] for c in '）)。、,　')]

print(f'ゴミ文字付きURL件数: {len(dirty_urls)}')
if dirty_urls:
    for lead in dirty_urls[:5]:
        print(f"  {lead.get('チャンネル名')}: {lead.get('問い合わせフォームURL')}")
else:
    print('✅ ゴミ文字は見つかりません')

print(f'\n総リード数: {len(leads)}')
print(f'A-rank (ランク=A): {len([l for l in leads if l.get("ランク") == "A"])}')
