import re

with open('target_scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ICPConfig クラスの値を更新
content = re.sub(
    r'min_subscribers\s*=\s*500',
    'min_subscribers = 200',
    content
)
content = re.sub(
    r'max_subscribers\s*=\s*50000',
    'max_subscribers = 80000',
    content
)
content = re.sub(
    r'min_recent_3m_videos\s*=\s*4',
    'min_recent_3m_videos = 2',
    content
)

with open('target_scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ ICP 閾値を更新しました:')
print('  min_subscribers: 500 → 200')
print('  max_subscribers: 50,000 → 80,000')
print('  min_recent_3m_videos: 4 → 2')
