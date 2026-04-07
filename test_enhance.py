import re
from email_extractor import _extract_urls_from_text, _get_website_via_ytdlp

# テスト1: _extract_urls_from_text()
test_text = """
公式サイト: https://example.com
ブログ: https://blog.example.co.jp
短縮URL: https://bit.ly/test
お問い合わせ: https://example.com/contact?param=value
"""

print("=" * 60)
print("テスト1: _extract_urls_from_text()")
print("=" * 60)
urls = _extract_urls_from_text(test_text)
for url in urls:
    print(f"✅ 抽出: {url}")

# テスト2: 実際のYouTubeチャンネルでテスト（サンプル）
print("\n" + "=" * 60)
print("テスト2: _get_website_via_ytdlp() - 実行準備")
print("=" * 60)
print("実際のチャンネルURL で動作確認します")
print("例: python -c \"from email_extractor import _get_website_via_ytdlp; print(_get_website_via_ytdlp('https://www.youtube.com/channel/CHANNEL_ID'))\"")
