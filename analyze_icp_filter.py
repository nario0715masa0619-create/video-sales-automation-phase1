with open('logs/collect.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ICP フィルタリング関連のログを抽出
for line in lines:
    if 'ICP' in line or 'フィルタリング' in line or '除外' in line or 'チャンネル候補' in line:
        print(line.rstrip())
