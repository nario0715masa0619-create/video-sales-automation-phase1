with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 29行目のインデントを修正
for i in range(len(lines)):
    if i >= 28 and i <= 31:  # 29-32行目付近
        if 'if os.getenv' in lines[i]:
            # インデントを正す（前の行と同じレベル）
            lines[i] = '            if os.getenv(\"YOUTUBE_API_KEY3\"):\n'
        elif 'self.api_keys.append' in lines[i] and 'YOUTUBE_API_KEY3' in lines[i]:
            lines[i] = '                self.api_keys.append(os.getenv(\"YOUTUBE_API_KEY3\"))\n'

with open('youtube_api_optimized.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ インデントを修正しました')
