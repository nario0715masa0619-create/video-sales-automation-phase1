import re

with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# upsert_lead メソッドを探す
match = re.search(r'def upsert_lead\(.*?\):\n(.*?)(?=\n    def |\nclass |\Z)', content, re.DOTALL)
if match:
    lines = match.group(0).split('\n')
    for i, line in enumerate(lines[:100]):
        print(line)
else:
    print('メソッド不見つ')
