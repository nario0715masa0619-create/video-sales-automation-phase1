import json
with open('cache/email_data.json','r',encoding='utf-8') as f:
    data = json.load(f)
    
    no_email_with_website = [d for d in data.values() if d.get('website') and not d.get('email')]
    
    print(f'Website ありメールなし: {len(no_email_with_website)} 件\n')
    print(f'フォーム URL 保有状況:')
    with_form = sum(1 for d in no_email_with_website if d.get('form_url'))
    print(f'  - フォーム URL あり: {with_form} 件')
    print(f'  - フォーム URL なし: {len(no_email_with_website) - with_form} 件')
    
    print(f'\n結論: フォーム送信でメール取得の可能性あり = {with_form} 件')
