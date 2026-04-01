with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# DEFAULT_SEARCH_KEYWORDS を幅広く設定
new_keywords = [
    'YouTube活用',
    '動画マーケティング',
    'オンライン営業',
    'SNS活用',
    '動画集客',
    'ウェビナー',
    'YouTube広告',
    'インフルエンサー',
    'チャンネル運用',
    'コンテンツマーケティング',
    'ビジネスYouTube',
    '企業動画',
]

import re
pattern = r"DEFAULT_SEARCH_KEYWORDS\s*=\s*\[.*?\]"
replacement = f"DEFAULT_SEARCH_KEYWORDS = {new_keywords}"
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ DEFAULT_SEARCH_KEYWORDS を更新しました')
