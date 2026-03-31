with open('logs/collect.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# DEBUG ログからスコアリング結果を抽出
scored_channels = []
for line in lines:
    if 'DEBUG' in line and 'calculate_score' in line:
        # チャンネル名を抽出
        if ':' in line:
            parts = line.split(' - ')
            if len(parts) > 1:
                ch_name = parts[1].split(':')[0].strip()
                scored_channels.append(ch_name)

unique_scored = set(scored_channels)
print(f'スコアリング対象チャンネル: {len(scored_channels)} 件')
print(f'ユニークなチャンネル: {len(unique_scored)} 件')
print(f'重複: {len(scored_channels) - len(unique_scored)} 件')

# 重複しているチャンネルを表示
from collections import Counter
counts = Counter(scored_channels)
duplicates = [ch for ch, count in counts.items() if count > 1]
print(f'\n重複チャンネル（最初の 10 件）:')
for ch in duplicates[:10]:
    print(f'  {ch}: {counts[ch]} 回')
