import re

with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# SERPAPI_KEY_INDEX を強制的に 1 に設定
content = re.sub(r'SERPAPI_KEY_INDEX\s*=\s*\d+', 'SERPAPI_KEY_INDEX = 1', content)

with open('config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ config.py を強制修正しました')
