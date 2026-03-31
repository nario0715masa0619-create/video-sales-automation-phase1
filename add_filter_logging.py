with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# filter_by_icp の呼び出し部分を修正
old_code = '''    passed_channels, rejected_channels = filter_by_icp(channels)
    channels = passed_channels
    logger.info(f"チャンネル候補: {len(channels)}件")'''

new_code = '''    passed_channels, rejected_channels = filter_by_icp(channels)
    logger.info(f"ICP フィルタリング前: {len(channels)}件")
    logger.info(f"ICP フィルタリング後: {len(passed_channels)}件（合格）")
    logger.info(f"ICP フィルタリング除外: {len(rejected_channels)}件（不合格）")
    if rejected_channels:
        logger.debug(f"除外されたチャンネル: {[ch.channel_name for ch in rejected_channels[:10]]}")
    channels = passed_channels
    logger.info(f"チャンネル候補: {len(channels)}件")'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ collect.py を修正しました')
print('  ICP フィルタリング結果をログに出力するようにしました')
