with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

print('=== 最終チェックリスト ===')

checks = [
    ('テストモード (5件)', 'scored_channels = scored_channels[:5]'),
    ('Step 7: get_email_from_youtube_channel', 'get_email_from_youtube_channel(channel_url)'),
    ('Step 7: ch.channel.contact_email', 'ch.channel.contact_email = email'),
    ('Step 7: JSON 保存', 'json.dump(email_data'),
    ('Step 6: JSON 読み込み', 'email_data_loop = json.load'),
    ('Step 6: メール割り当て', 'if ch.channel.channel_url in email_data_loop'),
    ('email_extractor import', 'from email_extractor import get_email_from_youtube_channel'),
    ('dry_run チェック', 'if not dry_run:'),
]

for name, check_str in checks:
    if check_str in content:
        print(f'✅ {name}')
    else:
        print(f'❌ {name}')
