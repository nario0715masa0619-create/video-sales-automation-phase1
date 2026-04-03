import sys
sys.path.insert(0, '.')
from email_extractor import get_email_from_youtube_channel
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# テストチャンネル（成功したやつと失敗したやつの両方）
test_urls = [
    'https://www.youtube.com/@OchiChannel',  # 失敗: おーち
    'https://www.youtube.com/c/pepacomi',     # 成功: kintone活用ちゃんねる
]

for url in test_urls:
    print(f'\n{'='*60}')
    print(f'テスト: {url}')
    print('='*60)
    website, email, form_url = get_email_from_youtube_channel(url)
    print(f'結果:')
    print(f'  公式サイト: {website or "取得失敗"}')
    print(f'  メール: {email or "未発見"}')
    print(f'  問い合わせURL: {form_url or "未発見"}')
