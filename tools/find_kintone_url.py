with open('logs/collect.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# kintone のチャンネルURL を探す
for line in lines:
    if 'kintone活用ちゃんねる' in line and 'チャンネルURL' in line:
        print(line.rstrip())
        break

# または channel_url の形式で探す
for line in lines:
    if 'kintone活用ちゃんねる' in line:
        print(line.rstrip())
