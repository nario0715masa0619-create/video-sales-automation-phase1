with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# SERPAPI_KEY_INDEX を検索
import re
match = re.search(r'SERPAPI_KEY_INDEX\s*=\s*(\d+)', content)
if match:
    current_index = match.group(1)
    print(f'現在の SERPAPI_KEY_INDEX: {current_index}')
else:
    print('SERPAPI_KEY_INDEX が見つかりません')

# SERPAPI_KEYS を検索
match = re.search(r'SERPAPI_KEYS\s*=\s*\[(.*?)\]', content, re.DOTALL)
if match:
    keys_str = match.group(1)
    keys = [k.strip().strip('\\"') for k in keys_str.split(',') if k.strip()]
    print(f'\n登録されている API キー数: {len(keys)}')
    for i, key in enumerate(keys):
        print(f'  KEY{i}: {key[:20]}...')
