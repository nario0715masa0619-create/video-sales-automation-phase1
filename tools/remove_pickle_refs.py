with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# pickle 関連のコードをすべて削除
content = content.replace(
    'with open("cache/scored_channels.pkl", "rb") as f:\n        scored_channels = pickle.load(f)',
    '# pickle は使用しないため削除'
)

# 他の pickle 参照を削除
import re
content = re.sub(r'with open\("cache/scored_channels\.pkl".*?\n.*?\)', '', content)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ pickle 参照を削除しました')
