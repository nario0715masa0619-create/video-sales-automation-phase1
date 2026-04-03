with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 7 ループの最初にデバッグログを追加（URL 形式確認用）
old_code = '''    logger.info("\n=== Step 7: メールアドレス自動取得 ===")
    email_count = 0
    for i, ch in enumerate(scored_channels):
        if i % 10 == 0 and i > 0:
            logger.info(f"進捗: {i}/{len(scored_channels)}")

        channel_url = ch.channel_url'''

new_code = '''    logger.info("\n=== Step 7: メールアドレス自動取得 ===")
    email_count = 0
    for i, ch in enumerate(scored_channels):
        if i % 10 == 0 and i > 0:
            logger.info(f"進捗: {i}/{len(scored_channels)}")

        channel_url = ch.channel_url
        # デバッグ：最初の5件の URL を表示
        if i < 5:
            logger.info(f"DEBUG URL {i+1}: {channel_url}")'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ チャンネル URL デバッグを追加しました')
