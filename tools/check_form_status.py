import json
import os

total_channels = 0
with_form = 0
no_form = 0
with_email_no_form = 0
no_email_with_form = 0

if os.path.exists('cache/email_data.json'):
    with open('cache/email_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        total_channels = len(data)
        for url, info in data.items():
            has_email = bool(info.get('email'))
            has_form = bool(info.get('form_url'))
            
            if has_form:
                with_form += 1
            else:
                no_form += 1
            
            if has_email and not has_form:
                with_email_no_form += 1
            elif not has_email and has_form:
                no_email_with_form += 1

print(f'総チャンネル: {total_channels}')
print(f'フォームURL取得済み: {with_form} ({with_form/total_channels*100:.1f}%)')
print(f'フォームなし: {no_form}')
print(f'メールあり&フォームなし: {with_email_no_form}')
print(f'メールなし&フォームあり: {no_email_with_form} <- 自動送信対象')
