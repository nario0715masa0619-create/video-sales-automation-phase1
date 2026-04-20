import json
with open('cache/email_data.json','r',encoding='utf-8') as f:
    data = json.load(f)
    with_email = sum(1 for d in data.values() if d.get('email'))
    print(f'200ch × IT: {with_email}/{len(data)} = {with_email/len(data)*100:.1f}%')
