from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

# 最終確認
dirty_urls = [l for l in leads if l.get('問い合わせフォームURL') and any(c in l['問い合わせフォームURL'] for c in '）)。、,　')]

print('=== 最終確認 ===')
print(f'総リード数: {len(leads)}')
print(f'ゴミ文字付きURL: {len(dirty_urls)}件')

if len(dirty_urls) == 0:
    print('✅ すべてのURLが正規化されました！')
else:
    print('❌ まだゴミ文字が残っています:')
    for lead in dirty_urls:
        print(f'  {lead.get("チャンネル名")}: {lead.get("問い合わせフォームURL")}')
