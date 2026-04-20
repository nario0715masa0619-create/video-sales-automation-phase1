import json

with open('cache/email_data.json','r',encoding='utf-8') as f:
    data = json.load(f)
    
    no_email = [(url, d) for url, d in data.items() if d.get('website') and not d.get('email')]
    
    print(f'Website あるのにメールなし: {len(no_email)} 件\n')
    print('サンプル（最初の10件）:')
    for i, (url, info) in enumerate(no_email[:10], 1):
        print(f'{i}. {info["website"]}')
