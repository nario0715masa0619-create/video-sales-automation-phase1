with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 6 ループの直前にメール情報を再度割り当て
old_code = '''    if not dry_run:
        for i, ch in enumerate(scored_channels):
            if i % 10 == 0 and i > 0:
                logger.info(f"進捗: {i}/{len(scored_channels)}")
            try:
                logger.debug(f"DEBUG ループ内 {i}: {ch.channel_name} - email={ch.contact_email} (直前)")
                lead_data = ch.to_crm_dict()'''

new_code = '''    if not dry_run:
        # JSON からメール情報を再度読み込む（ループ開始直前）
        import json
        email_data_loop = {}
        if os.path.exists("cache/email_data.json"):
            with open("cache/email_data.json", "r", encoding="utf-8") as f:
                email_data_loop = json.load(f)
        
        for i, ch in enumerate(scored_channels):
            # ループのたびにメール情報を割り当て
            if ch.channel_url in email_data_loop:
                ch.contact_email = email_data_loop[ch.channel_url].get('email', '')
                ch.website_url = email_data_loop[ch.channel_url].get('website', '')
                ch.contact_form_url = email_data_loop[ch.channel_url].get('form_url', '')
            
            if i % 10 == 0 and i > 0:
                logger.info(f"進捗: {i}/{len(scored_channels)}")
            try:
                logger.debug(f"DEBUG ループ内 {i}: {ch.channel_name} - email={ch.contact_email} (割り当て後)")
                lead_data = ch.to_crm_dict()'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 6 ループ内でメール情報を再度割り当てるようにしました')
