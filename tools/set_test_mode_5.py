with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# テストモードを 5件に設定
if 'scored_channels = scored_channels[:' in content:
    import re
    content = re.sub(r'scored_channels = scored_channels\[:\d+\]', 
                     'scored_channels = scored_channels[:5]', content)
else:
    # テストモードを追加
    content = content.replace(
        'logger.info(f"✅ スコアリング完了: {len(scored_channels)} 件")',
        'logger.info(f"✅ スコアリング完了: {len(scored_channels)} 件")\n    scored_channels = scored_channels[:5]\n    logger.info("⚠️  テストモード: 5件だけ処理します")'
    )

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ テストモードを 5件に設定しました')
