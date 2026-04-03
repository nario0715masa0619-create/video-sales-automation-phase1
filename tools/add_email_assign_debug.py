with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 7 のメール割り当て直後にデバッグコードを追加
old_code = '''            if email:
                logger.info(f\"✅ メール取得成功: {company_name} → {email}\")
                email_count += 1'''

new_code = '''            if email:
                logger.info(f\"✅ メール取得成功: {company_name} → {email}\")
                logger.debug(f\"DEBUG: ch.contact_email に設定: '{ch.contact_email}', email: '{email}'\")
                email_count += 1'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 7 のメール割り当てデバッグコードを追加しました')
