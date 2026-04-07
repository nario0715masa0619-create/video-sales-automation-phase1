with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 ループ開始（149行目）の直後にコードを挿入
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    # 149 行目（if not dry_run:）の直後に JSON 読み込みコードを挿入
    if i == 148 and 'if not dry_run:' in line:
        new_lines.append('        import json, os\n')
        new_lines.append('        email_data_loop = {}\n')
        new_lines.append('        if os.path.exists("cache/email_data.json"):\n')
        new_lines.append('            with open("cache/email_data.json", "r", encoding="utf-8") as f:\n')
        new_lines.append('                email_data_loop = json.load(f)\n')
        new_lines.append('        logger.debug(f"DEBUG: JSON から {len(email_data_loop)} 件のメール情報を読込")\n')
        new_lines.append('\n')

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ Step 6 ループ前に JSON 読み込みコードを挿入しました')
