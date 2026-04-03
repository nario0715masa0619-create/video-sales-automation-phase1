with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# argparse 部分を確認
for i, line in enumerate(lines):
    if "add_argument" in line and "dry" in line.lower():
        for j in range(max(0, i-1), min(i+5, len(lines))):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        break
