with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# スコアリング完了のログを探して、その直後に追加
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if 'スコアリング完了: {len(scored_channels)} 件' in line:
        new_lines.append('\n')
        new_lines.append('    # テストモード：5件だけ処理\n')
        new_lines.append('    scored_channels = scored_channels[:5]\n')
        new_lines.append('    logger.info("⚠️  テストモード: 5件だけ処理します")\n')

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ テストモード（5件）を手動で追加しました')
