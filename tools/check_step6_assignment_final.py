with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("=== Step 6 メール割り当て部分 ===")
for i, line in enumerate(lines):
    if "if ch.channel.channel_url in email_data_loop:" in line:
        for j in range(i-2, min(i+8, len(lines))):
            print(f"{j+1:4d}: {lines[j].rstrip()}")
        break
