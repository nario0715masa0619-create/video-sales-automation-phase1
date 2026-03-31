with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# channels = passed_channels の後に重複排除を追加
import re
content = re.sub(
    r'(channels = passed_channels)',
    r'\1\n    # URL で重複排除\n    unique_channels = {ch.channel.channel_url: ch for ch in channels}\n    channels = list(unique_channels.values())\n    logger.info(f"重複排除後: {len(channels)}件")',
    content
)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ collect.py に重複排除ロジックを追加しました')
