import re

# email_extractor.py の scrape_email_from_site() 内の JSON-LD 処理を置換
with open('email_extractor.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 古い JSON-LD 処理ブロックを特定して置換
# パターン: "JSON-LD スキーマからメール抽出" から "found_email =" までの範囲を置換

old_pattern = r'# JSON-LD スキーマからメール抽出.*?if email and \(EMAIL_PATTERN\.match\(email\) or EMAIL_PATTERN_JP\.match\(email\)\):.*?logger\.info\(f"JSON-LD でメール発見: \{email\}"\).*?found_email = email.*?break'

new_code = '''# JSON-LD スキーマからメール抽出（強化版）
                jsonld_emails = _extract_emails_from_jsonld_enhanced(html)
                if jsonld_emails:
                    found_email = jsonld_emails[0]
                    logger.info(f"✅ JSON-LD 強化版でメール発見: {found_email}")
                    break'''

# 正規表現で置換（DOTALL フラグ使用）
content_modified = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

# ファイルに書き込み
with open('email_extractor.py', 'w', encoding='utf-8') as f:
    f.write(content_modified)

print('✅ JSON-LD 強化版を scrape_email_from_site に統合しました')
