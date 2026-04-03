with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

insert_pos = None
for i, line in enumerate(lines):
    if 'Step 7 完了' in line and 'email_count' in line:
        insert_pos = i + 1
        break

if insert_pos:
    new_lines = [
        '\n',
        '    import pickle\n',
        '    os.makedirs("cache", exist_ok=True)\n',
        '    with open("cache/scored_channels.pkl", "wb") as f:\n',
        '        pickle.dump(scored_channels, f)\n',
        '    logger.info("✅ キャッシュ保存: scored_channels")\n',
    ]
    lines = lines[:insert_pos] + new_lines + lines[insert_pos:]
    
    with open('collect.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print('✅ collect.py を修正しました')
else:
    print('❌ 修正位置が見つかりません')
