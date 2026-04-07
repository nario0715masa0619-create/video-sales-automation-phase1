with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# クォータチェック部分を削除（current_quota_usage = api.quota_used の部分）
content = content.replace(
    '''    # クォータチェック: 90% 以上使用していたら処理を中断
    current_quota_usage = api.quota_used
    if current_quota_usage > 9000:
        logger.error(f"❌ クォータ不足により処理を中断します")
        logger.error(f"   使用量: {current_quota_usage:,}/10,000 ユニット")
        logger.error(f"   詳細: DEVELOPMENT.md の『クォータ管理』を参照")
        sys.exit(1)

    ''',
    ''
)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ クォータチェック部分を削除しました')
