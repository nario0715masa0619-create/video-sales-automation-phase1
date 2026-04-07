with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 6 ループ内に、割り当て直前のメール値ログを追加
old_code = '''     try:
                lead_data = ch.to_crm_dict()
                upsert_lead(lead_data)'''

new_code = '''     try:
                # デバッグ：メール情報を確認
                logger.debug(f"DEBUG Step 6ループ {i}: {ch.channel_name} - email before to_crm_dict: '{ch.contact_email}'")
                lead_data = ch.to_crm_dict()
                logger.debug(f"DEBUG Step 6ループ {i}: {ch.channel_name} - email in lead_data: '{lead_data.get('メールアドレス', 'NONE')}'")
                upsert_lead(lead_data)'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 6 ループのデバッグを追加しました')
