with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 6 ループの直後にデバッグを追加
old_code = '''    # Step 6: CRM 更新
    logger.info("\n=== Step 6: CRM 更新 ===")
    if not dry_run:
        for i, ch in enumerate(scored_channels):
            if i % 10 == 0 and i > 0:
                logger.info(f"進捗: {i}/{len(scored_channels)}")
            try:
                lead_data = ch.to_crm_dict()'''

new_code = '''    # Step 6: CRM 更新
    logger.info("\n=== Step 6: CRM 更新 ===")
    logger.info(f"DEBUG: Step 6 開始時の scored_channels 件数: {len(scored_channels)}")
    logger.info(f"DEBUG: 最初のチャンネルメール (Step 6直前): {scored_channels[0].contact_email if scored_channels else 'NONE'}")
    if not dry_run:
        for i, ch in enumerate(scored_channels):
            if i % 10 == 0 and i > 0:
                logger.info(f"進捗: {i}/{len(scored_channels)}")
            try:
                logger.debug(f"DEBUG ループ内 {i}: {ch.channel_name} - email={ch.contact_email} (直前)")
                lead_data = ch.to_crm_dict()'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 6 ループのデバッグを追加しました')
