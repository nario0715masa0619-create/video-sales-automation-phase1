with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# キャッシュ読込直後にデバッグコードを追加
old_code = '''    # Step 6 直前：キャッシュから scored_channels を再度読み込む
    with open(\"cache/scored_channels.pkl\", \"rb\") as f:
        scored_channels = pickle.load(f)
    logger.info(f\"✅ キャッシュ読込: {len(scored_channels)} 件のメール情報を確認\")
    
    # Step 6: CRM 更新'''

new_code = '''    # Step 6 直前：キャッシュから scored_channels を再度読み込む
    with open(\"cache/scored_channels.pkl\", \"rb\") as f:
        scored_channels = pickle.load(f)
    logger.info(f\"✅ キャッシュ読込: {len(scored_channels)} 件のメール情報を確認\")
    
    # デバッグ：キャッシュから読み込んだデータの確認
    logger.info(\"=== キャッシュ読込後のメール情報（最初の3件） ===\")
    for i, ch in enumerate(scored_channels[:3]):
        logger.info(f\"{i+1}. {ch.channel_name}: email='{ch.contact_email}', website='{ch.website_url}'\")
    
    # Step 6: CRM 更新'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ キャッシュ読込後のデバッグコードを追加しました')
