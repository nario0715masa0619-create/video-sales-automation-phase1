with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# SERPAPI_KEY_INDEX を 1 に変更
content = content.replace('SERPAPI_KEY_INDEX = 0', 'SERPAPI_KEY_INDEX = 1')

with open('config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ config.py を修正しました - KEY2 を使用するように変更')
