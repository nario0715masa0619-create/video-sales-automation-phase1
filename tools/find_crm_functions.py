with open("crm_manager.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("=== crm_manager.py の関数定義 ===")
for i, line in enumerate(lines):
    if line.strip().startswith("def "):
        print(f"{i+1:4d}: {line.rstrip()}")
