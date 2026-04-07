with open('target_scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# dataclass をインポート
if 'from dataclasses import dataclass' not in content:
    # import 部分を探して追加
    content = content.replace(
        'from typing import Optional',
        'from dataclasses import dataclass\nfrom typing import Optional'
    )

# ChannelData を dataclass に変更
old_class = 'class ChannelData:'
new_class = '@dataclass\nclass ChannelData:'

content = content.replace(old_class, new_class)

with open('target_scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ ChannelData を dataclass に変更しました')
