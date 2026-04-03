with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 202行目の後に デバッグコードを挿入
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if i == 201 and '=== Step 6: CRM 更新 ===' in line:  # 202行目（0ベース）
        new_lines.append('    logger.info(f"DEBUG: Step 6 開始時の scored_channels 件数: {len(scored_channels)}")\n')
        new_lines.append('    if scored_channels:\n')
        new_lines.append('        logger.info(f"DEBUG: 最初のチャンネルメール (Step 6直前): {scored_channels[0].contact_email}")\n')

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ Step 6 のデバッグコードを手動で追加しました')
