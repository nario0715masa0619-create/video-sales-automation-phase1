import re

with open('website_scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# コメントアウト部分を置き換え
old_code = """        # Google Sheets にも保存（email を含む）
        # append_to_gsheet_phase5(
            # result['company_name'],
            # result['phone_number'],
            # None,
            # result['status'],
            # result['url']
            # )"""

new_code = """        # Google Sheets にも保存（email を含む）
        append_to_gsheet_phase5(
            result['company_name'],
            result['phone_number'],
            result['email'],
            result['status'],
            result['url']
        )"""

content = content.replace(old_code, new_code)

with open('website_scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ website_scraper.py を修正しました")
