with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# スコアリング完了後にテストモードを追加
old_code = '''    logger.info(f"✅ スコアリング完了: {len(scored_channels)} 件")

    # Step 7: メールアドレス抽出'''

new_code = '''    logger.info(f"✅ スコアリング完了: {len(scored_channels)} 件")
    
    # テストモード：5件だけ処理
    scored_channels = scored_channels[:5]
    logger.info("⚠️  テストモード: 5件だけ処理します")

    # Step 7: メールアドレス抽出'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ テストモード（5件）を有効にしました')
