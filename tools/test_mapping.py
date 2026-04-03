# テスト: lead_data に website が含まれているか
lead_data = {
    "チャンネルURL": "https://example.com",
    "チャンネル名": "Test",
    "メールアドレス": "test@example.com",
    "公式サイト": "https://example.com/site",
    "問い合わせフォームURL": "https://example.com/contact"
}

# LEADS_COLUMNS マッピング
LEADS_COLUMNS = {
    "会社名": 1,
    "担当者名": 2,
    "メールアドレス": 3,
    "問い合わせフォームURL": 4,
    "公式サイト": 5,
}

row_data = [""] * 40
for col_name, col_index in LEADS_COLUMNS.items():
    row_data[col_index - 1] = lead_data.get(col_name, "")

print("=== row_data の内容 ===")
for i in range(6):
    print(f"Col {i+1}: {row_data[i]}")
