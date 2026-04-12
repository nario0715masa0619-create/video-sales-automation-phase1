import json
with open('cache/email_data.json','r',encoding='utf-8') as f:
    data = json.load(f)
    
    with_email = sum(1 for d in data.values() if d.get('email'))
    with_website = sum(1 for d in data.values() if d.get('website'))
    with_form = sum(1 for d in data.values() if d.get('form_url'))
    
    print(f'総チャンネル: {len(data)} 件')
    print(f'メール取得: {with_email} 件 ({with_email/len(data)*100:.1f}%)')
    print(f'Website 取得: {with_website} 件 ({with_website/len(data)*100:.1f}%)')
    print(f'フォーム URL 取得: {with_form} 件 ({with_form/len(data)*100:.1f}%)')
    print(f'\nWebsite があるのにメール なし: {sum(1 for d in data.values() if d.get("website") and not d.get("email"))} 件')
