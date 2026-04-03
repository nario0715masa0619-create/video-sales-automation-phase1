# Step 6 で upsert_lead() が呼ばれる直前に、lead_data を確認するコードを追加
with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# lead_data = ch.to_crm_dict() の直後にデバッグコードを挿入
for i, line in enumerate(lines):
    if "lead_data = ch.to_crm_dict()" in line:
        insert_pos = i + 1
        debug = '                logger.debug(f"DEBUG lead_data keys: {list(lead_data.keys())}")\n'
        lines.insert(insert_pos, debug)
        break

with open("collect.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("OK")
