with open("crm_manager.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# append_row 周辺を確認
for i, line in enumerate(lines):
    if "sheet.append_row" in line:
        print(f"=== append_row 周辺 ===")
        for j in range(max(0, i-20), min(i+2, len(lines))):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        break
