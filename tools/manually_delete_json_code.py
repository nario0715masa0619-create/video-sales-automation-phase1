with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 186-205行目（JSON 読込・割り当てコード）を削除
new_lines = []
skip_until = -1

for i, line in enumerate(lines):
    if i >= 185 and i <= 205:  # 186-206行目（0ベース）
        if '# Step 6 直前' in line or 'import json' in line or 'email_data = {}' in line or 'os.path.exists' in line or 'with open' in line or 'json.load' in line or 'for ch in scored_channels:' in line and i > 185 or 'if ch.channel_url in email_data' in line or 'ch.contact_email' in line and i > 185 or 'ch.website_url' in line and i > 185 or 'ch.contact_form_url' in line and i > 185 or 'logger.info(f"✅ メール情報読込' in line or '=== メール情報割り当て後' in line or (i > 185 and i < 206 and line.strip() == ''):
            continue
    new_lines.append(line)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ JSON 読込・割り当てコードを削除しました')
