with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 30行目（YOUTUBE_API_KEY2）の直後に KEY3 を追加
for i, line in enumerate(lines):
    if 'YOUTUBE_API_KEY2' in line and 'os.getenv' in line:
        lines.insert(i+1, '            if os.getenv(\"YOUTUBE_API_KEY3\"):\n')
        lines.insert(i+2, '                self.api_keys.append(os.getenv(\"YOUTUBE_API_KEY3\"))\n')
        break

with open('youtube_api_optimized.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ YOUTUBE_API_KEY3 を追加しました')
