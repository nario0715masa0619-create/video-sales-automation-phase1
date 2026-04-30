with open('website_scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# append_to_gsheet_phase5 呼び出しをコメントアウト
old_code = """        # Google Sheets にも保存（email を含む）
        append_to_gsheet_phase5(
            result['company_name'],
            result['phone_number'],
            result['email'],
            result['status'],
            result['url']
        )"""

new_code = """        # Google Sheets にはバッチ保存（レート制限回避）
        # append_to_gsheet_phase5(
        #     result['company_name'],
        #     result['phone_number'],
        #     result['email'],
        #     result['status'],
        #     result['url']
        # )"""

content = content.replace(old_code, new_code)

with open('website_scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ website_scraper.py の Google Sheet 呼び出しをコメントアウトしました')
