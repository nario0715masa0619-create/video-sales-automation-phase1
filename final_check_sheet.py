from crm_manager import CRMManager
crm = CRMManager()
leads = crm.get_all_leads()
print(f'=== スプレッドシート最終状態 ===')
print(f'総リード数: {len(leads)}')
a_rank = len([l for l in leads if l.get('ランク') == 'A'])
b_rank = len([l for l in leads if l.get('ランク') == 'B'])
c_rank = len([l for l in leads if l.get('ランク') == 'C'])
print(f'A-rank: {a_rank}')
print(f'B-rank: {b_rank}')
print(f'C-rank: {c_rank}')
print(f'合計: {a_rank + b_rank + c_rank}')

# メール取得件数
email_count = len([l for l in leads if l.get('メールアドレス')])
form_url_count = len([l for l in leads if l.get('問い合わせフォームURL')])
print(f'\nメールアドレス取得: {email_count}件')
print(f'問い合わせフォームURL取得: {form_url_count}件')
