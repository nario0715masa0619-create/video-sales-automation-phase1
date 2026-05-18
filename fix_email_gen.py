# email_generator.py を修正

with open('email_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# コメントアウトする行を探す
new_lines = []
skip_next = 0

for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        # コメント行を追加（ただし先頭のインデントは保持）
        if 'channel_name, latest_title, channel_description' in line or \
           'channel_name, videos_3m, avg_view, avg_engagement, trend, rank' in line or \
           (i > 0 and ')' in line and skip_next == 0):
            continue
        new_lines.append(line)
    elif 'personalized["video_comment"] = _generate_video_comment(' in line:
        # この行をコメントアウト
        new_lines.append(line.replace('personalized["video_comment"]', '# personalized["video_comment"]'))
        skip_next = 2  # 次の2行もスキップ
    elif 'personalized["improvement_hint"] = _generate_improvement_hint(' in line:
        # この行をコメントアウト
        new_lines.append(line.replace('personalized["improvement_hint"]', '# personalized["improvement_hint"]'))
        skip_next = 2  # 次の2行もスキップ
    else:
        new_lines.append(line)

with open('email_generator.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ email_generator.py を修正しました')
