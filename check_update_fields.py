with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# update_fields の定義を探す
import re
match = re.search(r'update_fields\s*=\s*\{(.*?)\}', content, re.DOTALL)
if match:
    print('=== update_fields の内容 ===')
    print(match.group(0)[:1500])
else:
    print('update_fields が見つかりません')
