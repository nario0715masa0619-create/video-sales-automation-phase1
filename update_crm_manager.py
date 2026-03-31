with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# update_fields の定義を修正
# "最新動画タイトル" の後に "問い合わせフォームURL" を追加
old_pattern = '''                "最新動画タイトル": lead_data.get("最新動画タイトル", old_record.get("最新動画タイトル", "")),
                "最終更新日": now,'''

new_pattern = '''                "最新動画タイトル": lead_data.get("最新動画タイトル", old_record.get("最新動画タイトル", "")),
                "問い合わせフォームURL": lead_data.get("問い合わせフォームURL", old_record.get("問い合わせフォームURL")),
                "メールアドレス": lead_data.get("メールアドレス", old_record.get("メールアドレス")),
                "最終更新日": now,'''

content = content.replace(old_pattern, new_pattern)

with open('crm_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ crm_manager.py を修正しました')
print('  - 問い合わせフォームURL を update_fields に追加')
print('  - メールアドレス を update_fields に追加')
