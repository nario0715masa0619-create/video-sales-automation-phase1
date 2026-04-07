with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 6 ループの crm_dict 生成直後にデバッグ出力を追加
old_code = '''            try:
                lead_data = ch.to_crm_dict()
                upsert_lead(lead_data)'''

new_code = '''            try:
                lead_data = ch.to_crm_dict()
                # デバッグ：メール情報を確認
                if i < 3 or lead_data.get('メールアドレス'):
                    logger.debug(f"DEBUG Step 6: {lead_data.get('チャンネル名')} - メール='{lead_data.get('メールアドレス', 'EMPTY')}'")
                upsert_lead(lead_data)'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 6 デバッグ出力を追加しました')
