with open("target_scraper.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def to_crm_dict" in line:
        for j in range(i, min(i+13, len(lines))):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        break
