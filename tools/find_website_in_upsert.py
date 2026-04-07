with open("crm_manager.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# upsert_lead 関数を探す（最初の定義）
for i, line in enumerate(lines):
    if "def upsert_lead" in line and "lead_data" in line:
        for j in range(i, min(i+100, len(lines))):
            if "公式サイト" in lines[j] or "website" in lines[j].lower():
                print(f"{j+1:4d}: {lines[j].rstrip()}")
        break
