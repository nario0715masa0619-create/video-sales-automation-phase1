with open("crm_manager.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# LEADS_COLUMNS を探す
for i, line in enumerate(lines):
    if "LEADS_COLUMNS" in line and "=" in line:
        print(f"=== LEADS_COLUMNS ===")
        for j in range(i, min(i+20, len(lines))):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
            if "}" in lines[j]:
                break
        break
