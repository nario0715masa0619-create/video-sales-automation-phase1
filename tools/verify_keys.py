with open("youtube_api_optimized.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("=== API KEY 確認 ===")
for i, line in enumerate(lines):
    if "YOUTUBE_API_KEY" in line and "getenv" in line:
        print(f"{i+1:4d}: {lines[i].rstrip()}")
