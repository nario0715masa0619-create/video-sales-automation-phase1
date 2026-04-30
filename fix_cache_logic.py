with open('website_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# DB チェック部分を見つけて修正
modified = []
for i, line in enumerate(lines):
    if 'if check_url_exists(website_url):' in line:
        # この行とその後の 3 行を置き換え
        modified.append(line)
        modified.append(lines[i+1])  # logger.info の行
        modified.append(lines[i+2])  # skipped_count += 1 の行
        modified.append(lines[i+3])  # continue の行
        
        # 新しいロジックに置き換え
        modified.pop()  # continue を削除
        modified.pop()  # skipped_count += 1 を削除
        modified.pop()  # logger.info を削除
        modified.pop()  # if を削除
        
        # 新しいロジックを追加
        modified.append('        if check_url_exists(website_url):\n')
        modified.append('            # キャッシュが有効か確認\n')
        modified.append('            from tools.html_fetcher import get_cached_html\n')
        modified.append('            cached = get_cached_html(website_url, ttl_hours=168)\n')
        modified.append('            if cached:\n')
        modified.append('                logger.info(f"⏭️  既存 URL スキップ（キャッシュ有効）: {website_url}")\n')
        modified.append('                skipped_count += 1\n')
        modified.append('                continue\n')
        modified.append('            else:\n')
        modified.append('                logger.info(f"🔄 キャッシュ期限切れ - 再クロール: {website_url}")\n')
        
        # 次の 3 行をスキップ
        continue
    elif i > 0 and 'if check_url_exists(website_url):' in lines[i-3]:
        # 既に処理済みの行をスキップ
        if i - 4 < len(lines) and 'if check_url_exists' in lines[i-4]:
            continue
    else:
        modified.append(line)

with open('website_scraper.py', 'w', encoding='utf-8') as f:
    f.writelines(modified)

print('✅ DB チェック ロジックを修正しました')
