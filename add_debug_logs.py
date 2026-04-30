import re

with open('website_scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# インポートに time を追加
if 'import time' not in content:
    content = content.replace('import logging', 'import logging\nimport time')

# run_batch_scraping 関数内に計測ロジックを追加
# 「success_count = 0」の行の後に「start_time = time.time()」を追加
content = content.replace(
    'success_count = 0\n    email_count = 0\n    skipped_count = 0',
    'success_count = 0\n    email_count = 0\n    skipped_count = 0\n    \n    start_time = time.time()'
)

# ループ内に計測を追加
# 「for idx, url_data in enumerate(url_list, 1):」の後に追加
content = content.replace(
    'for idx, url_data in enumerate(url_list, 1):',
    'for idx, url_data in enumerate(url_list, 1):\n        loop_start = time.time()'
)

# ループ内の最後に経過時間ログを追加
# 「if result['email']:」の後に追加
content = content.replace(
    'if result[\'email\']:\n            email_count += 1',
    'if result[\'email\']:\n            email_count += 1\n        \n        if idx % 20 == 0:\n            loop_elapsed = time.time() - loop_start\n            logger.info(f\'⏱️  進捗: {idx}/{len(url_list)} | 最後の処理: {loop_elapsed:.2f}秒\')'
)

# 最後に総実行時間を追加
# 最後の logger.info の後に追加
content = content.replace(
    'logger.info(f"📊 結果: 成功 {success_count} | メール {email_count} | スキップ {skipped_count}")',
    'logger.info(f"📊 結果: 成功 {success_count} | メール {email_count} | スキップ {skipped_count}")\n    \n    total_elapsed = time.time() - start_time\n    logger.info(f"⏱️  総実行時間: {total_elapsed:.1f}秒 ({len(url_list)}件 / {total_elapsed/len(url_list):.2f}秒/件)")'
)

with open('website_scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ デバッグログを追加しました')
