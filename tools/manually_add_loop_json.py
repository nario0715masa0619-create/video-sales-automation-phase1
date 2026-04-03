with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 206行目（0ベース）の後に JSON 読込コードを挿入
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if i == 205 and 'if not dry_run:' in line:
        new_lines.append('        # JSON からメール情報を再度読み込む（ループ開始直前）\n')
        new_lines.append('        import json\n')
        new_lines.append('        email_data_loop = {}\n')
        new_lines.append('        if os.path.exists("cache/email_data.json"):\n')
        new_lines.append('            with open("cache/email_data.json", "r", encoding="utf-8") as f:\n')
        new_lines.append('                email_data_loop = json.load(f)\n')
        new_lines.append('\n')

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ JSON 読込コードをループ内に追加しました')
