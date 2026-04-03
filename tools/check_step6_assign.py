with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Step 6 ループのメール割り当て部分を表示
print("=== Step 6 メール割り当て部分 ===")
for i, line in enumerate(lines):
    if "if ch.channel.channel_url in email_data_loop:" in line:
        for j in range(i, min(i+6, len(lines))):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        break
