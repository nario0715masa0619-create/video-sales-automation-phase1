from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

# ゴミ文字の最終確認
dirty_urls = [l for l in leads if l.get('問い合わせフォームURL') and any(c in l['問い合わせフォームURL'] for c in '）)。、,　')]
print(f'ゴミ文字付きURL: {len(dirty_urls)}件')
if dirty_urls:
    for lead in dirty_urls:
        print(f'  {lead.get("チャンネル名")}: {lead.get("問い合わせフォームURL")}')
else:
    print('✅ ゴミ文字なし - クリア！')
