with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 間違った行を修正
content = content.replace(
    'unique_channels = {ch.channel.channel_url: ch for ch in channels}',
    'unique_channels = {ch.channel_url: ch for ch in channels}'
)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ 属性名を修正しました')
