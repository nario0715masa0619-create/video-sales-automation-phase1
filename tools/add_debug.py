with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 154行目（0-indexed では 153）の直後に挿入
insert_pos = 154  # 1-indexed

debug_code = '''    logger.info("\n=== 🔍 Step 7 デバッグ: メール情報確認（キャッシュ保存後） ===")
    with open('cache/scored_channels.pkl', 'rb') as f:
        debug_channels = pickle.load(f)
    for i, ch in enumerate(debug_channels[:5]):
        crm_dict = ch.to_crm_dict()
        logger.info(f"{i+1}. {ch.channel_name}")
        logger.info(f"   ch.contact_email: '{ch.contact_email}'")
        logger.info(f"   to_crm_dict()['contact_email']: '{crm_dict.get('contact_email', 'NOT_FOUND')}'")
        logger.info(f"   to_crm_dict()['contact_form_url']: '{crm_dict.get('contact_form_url', 'NOT_FOUND')}'")
'''

# 154行目の直後に挿入
new_lines = lines[:insert_pos] + [debug_code] + lines[insert_pos:]

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ デバッグコードを154行目の直後に挿入しました')
