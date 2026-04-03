with open('email_extractor.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# get_email_from_youtube_channel 関数を検索
for i, line in enumerate(lines):
    if 'def get_email_from_youtube_channel' in line:
        # 関数の最初の50行を表示
        for j in range(i, min(i+50, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
