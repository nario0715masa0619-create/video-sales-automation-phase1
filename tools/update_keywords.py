with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# キーワードを幅広く設定
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
pattern = r"SEARCH_KEYWORDS\s*=\s*\[.*?\]"
replacement = f"SEARCH_KEYWORDS = {new_keywords}"
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ config.py のキーワードを更新しました')
print(f'新キーワード: {new_keywords}')
