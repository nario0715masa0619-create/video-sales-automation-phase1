with open("utils.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def validate_crm_data_saved" in line:
        for j in range(i, min(i+40, len(lines))):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        break
