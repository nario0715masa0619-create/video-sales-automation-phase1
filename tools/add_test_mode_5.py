with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# スコアリング完了後にテストモードを追加
for i in range(len(lines)):
    if 'スコアリング完了:' in lines[i] and 'len(scored_channels)' in lines[i]:
        # このログの次の行に挿入
        insert_pos = i + 1
        test_mode_code = '''    
    # テストモード: 5件だけ処理
    scored_channels = scored_channels[:5]
    logger.info("⚠️  テストモード: 5件だけ処理します")
'''
        lines.insert(insert_pos, test_mode_code)
        break

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ テストモード (5件) を追加しました')
