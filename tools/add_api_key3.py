with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# API_KEYS = [...] の部分を探して修正
for i, line in enumerate(lines):
    if 'API_KEYS = [' in line:
        # 次の行から YOUTUBE_API_KEY を探す
        for j in range(i, min(i+5, len(lines))):
            if 'YOUTUBE_API_KEY' in lines[j] and 'YOUTUBE_API_KEY2' not in lines[j]:
                # その後に KEY3 を追加
                if 'YOUTUBE_API_KEY2' in lines[j+1]:
                    # KEY2 の後に KEY3 を追加
                    lines.insert(j+2, '            os.getenv(\"YOUTUBE_API_KEY3\"),\n')
                    break
        break

with open('youtube_api_optimized.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ YOUTUBE_API_KEY3 を youtube_api_optimized.py に追加しました')
