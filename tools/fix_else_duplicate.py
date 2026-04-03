with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 192-194 行目（デバッグコード）を削除、195行目の重複を削除
new_lines = []
skip_lines = {191, 192, 193, 194}  # 0ベース では 191-194

for i, line in enumerate(lines):
    if i in skip_lines:
        continue
    # 195行目の重複を1つだけ保持
    if i == 194 and line.strip() == "else:":
        if i == 0 or lines[i-1].strip() != "else:":
            new_lines.append(line)
    else:
        new_lines.append(line)

with open("collect.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("OK")
