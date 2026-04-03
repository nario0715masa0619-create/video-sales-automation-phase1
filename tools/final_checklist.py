with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

print('=== 最終チェックリスト ===')

# 1. テストモード確認
if 'scored_channels = scored_channels[:5]' in content:
    print('✅ テストモード: 5件処理')
else:
    print('❌ テストモード: 無効（全件処理）')

# 2. Step 7 のメール割り当て確認
if 'ch.channel.contact_email = email if email else' in content:
    print('✅ Step 7: ch.channel.contact_email に修正済み')
else:
    print('❌ Step 7: メール割り当て が未修正')

# 3. Step 6 のメール割り当て確認
if 'ch.channel.contact_email = email_data_loop' in content:
    print('✅ Step 6: ch.channel.contact_email に修正済み')
else:
    print('❌ Step 6: メール割り当て が未修正')

# 4. JSON 保存時のメール参照確認
if 'ch.channel.contact_email' in content and 'email_data[ch.channel.channel_url]' in content:
    print('✅ JSON保存: ch.channel 参照に修正済み')
else:
    print('❌ JSON保存: メール参照 が未修正')

# 5. get_email_from_youtube_channel の import 確認
if 'from email_extractor import get_email_from_youtube_channel' in content:
    print('✅ email_extractor: import済み')
else:
    print('❌ email_extractor: import なし')

# 6. dry_run フラグの確認
if 'dry_run' in content:
    print('✅ dry_run: フラグ存在')
else:
    print('❌ dry_run: フラグ なし')

# 7. クォータチェック削除確認
if 'current_quota_usage = youtube_api.quota_used' in content:
    print('⚠️  クォータチェック: まだ存在（削除推奨）')
else:
    print('✅ クォータチェック: 削除済み')
