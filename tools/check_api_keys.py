with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    content = f.read()

# API_KEYS の定義部分を探す
import re
match = re.search(r'API_KEYS\s*=\s*\[(.*?)\]', content, re.DOTALL)
if match:
    api_keys_section = match.group(1)
    print('=== API_KEYS の定義 ===')
    print(api_keys_section)
else:
    print('API_KEYS が見つかりません')
