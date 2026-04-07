with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 7 完了からStep 6 開始までをシンプルにする
old_pattern = r'logger\.info\(f"✅ メール情報保存:.*?\n.*?# .*?\n.*?for i, ch in enumerate\(scored_channels\[:3\]\):.*?# Step 6: CRM 更新'

new_code = '''logger.info(f"✅ メール情報保存: {len(email_data)} 件 を JSON に保存")

    # Step 6: CRM 更新'''

import re
content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Step 7～Step 6 間のコードをシンプルに修正しました')
