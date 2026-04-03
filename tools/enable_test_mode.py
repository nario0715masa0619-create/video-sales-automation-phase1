with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# スコアリング完了の行を探す
for i, line in enumerate(lines):
    if 'スコアリング完了: {len(scored_channels)}' in line:
        # その直後に1件制限コードを挿入
        insert_pos = i + 2
        new_lines = [
            '\n',
            '    # テストモード：1件だけ処理\n',
            '    scored_channels = scored_channels[:1]\n',
            '    logger.info(f\"⚠️  テストモード: 1件だけ処理します\")\n',
        ]
        lines = lines[:insert_pos] + new_lines + lines[insert_pos:]
        break

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ テストモード（1件のみ）を有効化しました')
