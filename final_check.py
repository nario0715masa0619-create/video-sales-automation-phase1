import json
with open('cache/email_data.json','r',encoding='utf-8') as f:
    data = json.load(f)
    with_email = sum(1 for d in data.values() if d.get('email'))
    google_count = sum(1 for d in data.values() if 'google.com' in d.get('email', '').lower())
    valid_emails = with_email - google_count
    
    print(f'総チャンネル: {len(data)} 件')
    print(f'メール取得: {with_email} 件（Google: {google_count}, 正規メール: {valid_emails}）')
    print(f'成功率: {valid_emails/len(data)*100:.1f}%')
    print(f'\n正規メール例（最初の15件）:')
    count = 0
    for url, info in data.items():
        if info.get('email') and 'google.com' not in info.get('email', '').lower():
            print(f'  {info["email"]}')
            count += 1
            if count >= 15:
                break
