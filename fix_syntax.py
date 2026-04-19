# ファイルを読む
with open('email_extractor.py', 'r', encoding='utf-8') as f:
    content = f.read()

# シンプルな置換
content = content.replace("rstrip('.,;:)\\]\\\"\\'')", "rstrip(r'.,;:)\\]\\\"\\'')")

# ファイルに書き込む
with open('email_extractor.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("修正完了")
