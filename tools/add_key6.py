with open("youtube_api_optimized.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# KEY5 の追加箇所を探して、その後に KEY6 を追加
for i, line in enumerate(lines):
    if 'YOUTUBE_API_KEY5' in line and 'getenv' in line:
        # この行の後に KEY6 を追加
        insert_pos = i + 2
        key6_line = '            if os.getenv("YOUTUBE_API_KEY6"):\n'
        key6_append = '                self.api_keys.append(os.getenv("YOUTUBE_API_KEY6"))\n'
        lines.insert(insert_pos, key6_line)
        lines.insert(insert_pos + 1, key6_append)
        break

with open("youtube_api_optimized.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("OK")
