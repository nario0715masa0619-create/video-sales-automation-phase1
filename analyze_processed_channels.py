import re

with open('logs/collect.log', 'r', encoding='utf-8') as f:
    log_content = f.read()

# リード更新のログから処理されたチャンネル名を抽出
processed_channels = re.findall(r'リード更新: (.*?) \(', log_content)
unique_channels = set(processed_channels)

print(f'処理されたユニークなチャンネル数: {len(unique_channels)}')
print(f'同じチャンネルが何度も更新された（重複処理）: {len(processed_channels) - len(unique_channels)}回')

# 重複が多いチャンネルを見つける
from collections import Counter
channel_counts = Counter(processed_channels)
print('\n最も更新されたチャンネル（上位 10 件）:')
for channel, count in channel_counts.most_common(10):
    print(f'  {channel}: {count}回')
