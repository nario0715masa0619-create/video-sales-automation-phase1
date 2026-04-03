with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 6 の直前に、キャッシュから scored_channels を再度読み込む
old_code = '''    logger.info(f\"✅ Step 7 完了: {email_count} 件のメール取得\")

    import pickle
    os.makedirs(\"cache\", exist_ok=True)
    with open(\"cache/scored_channels.pkl\", \"wb\") as f:
        pickle.dump(scored_channels, f)
    logger.info(\"✅ キャッシュ保存: scored_channels\")
    # Step 6: CRM 更新
    logger.info(\"\\n=== Step 6: CRM 更新 ===\")'''

new_code = '''    logger.info(f\"✅ Step 7 完了: {email_count} 件のメール取得\")

    import pickle
    os.makedirs(\"cache\", exist_ok=True)
    with open(\"cache/scored_channels.pkl\", \"wb\") as f:
        pickle.dump(scored_channels, f)
    logger.info(\"✅ キャッシュ保存: scored_channels\")
    
    # Step 6 直前：キャッシュから scored_channels を再度読み込む
    with open(\"cache/scored_channels.pkl\", \"rb\") as f:
        scored_channels = pickle.load(f)
    logger.info(f\"✅ キャッシュ読込: {len(scored_channels)} 件のメール情報を確認\")
    
    # Step 6: CRM 更新
    logger.info(\"\\n=== Step 6: CRM 更新 ===\")'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ キャッシュ読込処理を Step 6 直前に追加しました')
