with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 25行目までは保持、その後を正しく構成
keep_lines = lines[:26]

# 26行目以降を正しく追加
new_section = [
    '        # API キーの優先順位: 引数 > YOUTUBE_API_KEY > YOUTUBE_API_KEY2 > YOUTUBE_API_KEY3\n',
    '        self.api_keys = []\n',
    '        if api_key:\n',
    '            self.api_keys.append(api_key)\n',
    '        else:\n',
    '            if os.getenv("YOUTUBE_API_KEY"):\n',
    '                self.api_keys.append(os.getenv("YOUTUBE_API_KEY"))\n',
    '            if os.getenv("YOUTUBE_API_KEY2"):\n',
    '                self.api_keys.append(os.getenv("YOUTUBE_API_KEY2"))\n',
    '            if os.getenv("YOUTUBE_API_KEY3"):\n',
    '                self.api_keys.append(os.getenv("YOUTUBE_API_KEY3"))\n',
]

# 元のファイルから必要な部分を探す
rest_start = None
for i, line in enumerate(lines):
    if 'if not self.api_keys:' in line:
        rest_start = i
        break

if rest_start:
    final_lines = keep_lines + new_section + lines[rest_start:]
else:
    final_lines = keep_lines + new_section

with open('youtube_api_optimized.py', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print('✅ youtube_api_optimized.py を修正しました')
