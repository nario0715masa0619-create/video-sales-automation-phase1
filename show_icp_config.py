with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# ICP関連の設定値を抽出
print('=== ICP フィルタリング設定 ===')
for pattern in ['ICP_MIN_SUBSCRIBERS', 'ICP_MAX_SUBSCRIBERS', 'ICP_MIN_VIDEOS_3M', 'ICP_COUNTRY']:
    match = re.search(f'{pattern}\\s*=\\s*(.+)', content)
    if match:
        print(f'{pattern} = {match.group(1)}')
