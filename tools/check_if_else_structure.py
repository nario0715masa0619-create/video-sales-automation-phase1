with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Step 6 CRM更新 の if-else 構造を表示
for i, line in enumerate(lines):
    if "# Step 6: CRM 更新" in line:
        for j in range(i, min(i+50, len(lines))):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
            if "else:" in lines[j] and j > i+10:
                for k in range(j, min(j+5, len(lines))):
                    print(f"{k+1:4d}: {lines[k].rstrip()}")
                break
        break
