# Step 6 ループの直後に以下を追加して実行
with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# CRM 更新完了後、scored_channels の website_url を確認するコードを追加
for i, line in enumerate(lines):
    if "✅ CRM 更新:" in line:
        insert_pos = i + 1
        check_code = """
    # デバッグ: メモリ上のデータを確認
    print("=== scored_channels のメモリ内容 ===")
    for ch in scored_channels[:2]:
        print(f"{ch.channel.channel_name}: website={ch.channel.website_url}")
"""
        lines.insert(insert_pos, check_code)
        break

with open("collect.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("OK")
