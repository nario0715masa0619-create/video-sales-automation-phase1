import json
with open('cache/email_data.json','r',encoding='utf-8') as f:
    data = json.load(f)
    with_email = sum(1 for d in data.values() if d.get('email'))
    print(f'総チャンネル: {len(data)} 件')
    print(f'メール取得: {with_email} 件')
    print(f'成功率: {with_email/len(data)*100:.1f}%')
    print(f'\nメール取得成功例（最初の10件）:')
    count = 0
    for url, info in data.items():
        if info.get('email') and 'google.com' not in info.get('email', ''):
            print(f'  {info["email"]}')
            count += 1
            if count >= 10:
                break
