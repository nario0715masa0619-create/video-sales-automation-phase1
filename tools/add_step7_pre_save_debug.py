with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 7 ループの最後に、保存前のデバッグ出力を追加
old_code = '''    logger.info(f"✅ Step 7 完了: {email_count} 件のメール取得")

    import pickle'''

new_code = '''    logger.info(f"✅ Step 7 完了: {email_count} 件のメール取得")
    
    # デバッグ：保存前の scored_channels を確認
    logger.info("=== Step 7 完了後、保存直前のメール情報（最初の3件） ===")
    for i, ch in enumerate(scored_channels[:3]):
        logger.info(f"{i+1}. {ch.channel_name}: email='{ch.contact_email}', website='{getattr(ch, 'website_url', 'NONE')}'")

    import pickle'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 7 保存前デバッグ出力を追加しました')
