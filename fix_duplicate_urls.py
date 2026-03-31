with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# all_urls.extend(urls) の後に重複排除ロジックを追加
old_code = '''    all_urls = []
    for keyword in keywords:
        current_key = config.SERPAPI_KEYS[config.SERPAPI_KEY_INDEX]
        urls = search_company_channels(keyword, current_key)
        all_urls.extend(urls)

    channels = []
    for url in all_urls:'''

new_code = '''    all_urls = []
    for keyword in keywords:
        current_key = config.SERPAPI_KEYS[config.SERPAPI_KEY_INDEX]
        urls = search_company_channels(keyword, current_key)
        all_urls.extend(urls)

    # 重複 URL を除去
    all_urls = list(set(all_urls))
    logger.info(f"検索結果URL: {len(all_urls)}件（重複排除済み）")

    channels = []
    for url in all_urls:'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ collect.py を修正しました - URL重複排除処理を追加')
