with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# if __name__ == "__main__": 以降を表示
for i, line in enumerate(lines):
    if 'if __name__ == "__main__"' in line:
        for j in range(i, min(i+30, len(lines))):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        break
