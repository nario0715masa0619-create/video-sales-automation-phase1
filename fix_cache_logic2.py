import re

with open('website_scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修正前のブロック（完全一致で検索）
old_block = '''        if check_url_exists(website_url):
            logger.info(f"⏭️  既存 URL スキップ: {website_url}")
            skipped_count += 1
            continue'''

# 修正後のブロック
new_block = '''        if check_url_exists(website_url):
            # キャッシュが有効か確認
            from tools.html_fetcher import get_cached_html
            cached = get_cached_html(website_url, ttl_hours=168)
            if cached:
                logger.info(f"⏭️  既存 URL スキップ（キャッシュ有効）: {website_url}")
                skipped_count += 1
                continue
            else:
                logger.info(f"🔄 キャッシュ期限切れ - 再クロール: {website_url}")'''

# 置き換え実行
if old_block in content:
    content = content.replace(old_block, new_block)
    with open('website_scraper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ DB チェック ロジックを修正しました')
else:
    print('❌ 修正対象のコードが見つかりませんでした')
    print('website_scraper.py の行 125 付近を確認してください')
