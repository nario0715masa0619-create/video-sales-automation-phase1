with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 ループの前に JSON 読み込みコードを挿入（Line 169 の if not dry_run: の直後）
for i in range(len(lines)):
    if i == 168 and 'if not dry_run:' in lines[i]:
        # 169 行目の直後に挿入
        insert_code = '''        import json
        email_data_loop = {}
        if os.path.exists("cache/email_data.json"):
            with open("cache/email_data.json", "r", encoding="utf-8") as f:
                email_data_loop = json.load(f)
        logger.debug(f"DEBUG: JSON から {len(email_data_loop)} 件のメール情報を読込")

'''
        lines.insert(i+1, insert_code)
        break

# Step 6 ループ内でメール割り当てコードを挿入
for i in range(len(lines)):
    if 'for i, ch in enumerate(scored_channels):' in lines[i] and i > 160:
        # このループの直後に挿入
        insert_code = '''            # JSON からメール情報を割り当て
            if ch.channel.channel_url in email_data_loop:
                ch.channel.contact_email = email_data_loop[ch.channel.channel_url].get("email", "")
                ch.channel.website_url = email_data_loop[ch.channel.channel_url].get("website", "")
                ch.channel.contact_form_url = email_data_loop[ch.channel.channel_url].get("form_url", "")

'''
        lines.insert(i+1, insert_code)
        break

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ Step 6 にメール割り当てコードを追加しました')
