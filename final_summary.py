from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

# 最終的な統計
a_rank = len([l for l in leads if l.get('ランク') == 'A'])
b_rank = len([l for l in leads if l.get('ランク') == 'B'])
c_rank = len([l for l in leads if l.get('ランク') == 'C'])

print('=== 最終的な CRM データ ===')
print(f'総リード数: {len(leads)}')
print(f'A-rank: {a_rank}')
print(f'B-rank: {b_rank}')
print(f'C-rank: {c_rank}')

# ゴミ文字のある URL を再確認
dirty_urls = [l for l in leads if l.get('問い合わせフォームURL') and any(c in l['問い合わせフォームURL'] for c in '）)。、,　')]
print(f'\nゴミ文字付きURL: {len(dirty_urls)}件')
if dirty_urls:
    for lead in dirty_urls:
        print(f'  {lead.get("チャンネル名")}: {lead.get("問い合わせフォームURL")}')

# メールアドレスが取得できているか確認
with_email = len([l for l in leads if l.get('メールアドレス')])
print(f'\nメールアドレス取得済み: {with_email}件')

# 問い合わせフォームURL が取得できているか確認
with_contact_form = len([l for l in leads if l.get('問い合わせフォームURL')])
print(f'問い合わせフォームURL取得済み: {with_contact_form}件')
