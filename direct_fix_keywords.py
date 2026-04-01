with open('config.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 行 152-165 を置き換え
new_keywords = '''DEFAULT_SEARCH_KEYWORDS: list[str] = [
    "YouTube活用",
    "動画マーケティング",
    "オンライン営業",
    "SNS活用",
    "動画集客",
    "ウェビナー",
    "YouTube広告",
    "インフルエンサー",
    "チャンネル運用",
    "コンテンツマーケティング",
    "ビジネスYouTube",
    "企業動画",
]
'''

new_lines = lines[:151] + [new_keywords + '\n'] + lines[166:]

with open('config.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ DEFAULT_SEARCH_KEYWORDS を直接修正しました')
