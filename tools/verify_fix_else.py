with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(160, min(200, len(lines))):
    print(f"{i+1:4d}: {lines[i].rstrip()}")
