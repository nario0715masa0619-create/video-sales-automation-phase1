with open('email_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# _build_email_1 を抽出
import re
match = re.search(r'def _build_email_1\(.*?\n(?:.*?\n)*?    return EmailContent\(.*?\)', content, re.DOTALL)

if match:
    current_code = match.group(0)
    print('=== 現在の _build_email_1 ===')
    print(current_code)
else:
    print('関数が見つかりません')
