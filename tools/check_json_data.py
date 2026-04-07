import json

with open("cache/email_data.json", "r", encoding="utf-8") as f:
    email_data = json.load(f)

print("=== JSON に保存されたデータ ===")
for url, data in email_data.items():
    print(f"URL: {url}")
    print(f"  Email: {data.get('email', 'NONE')}")
    print(f"  Website: {data.get('website', 'NONE')}")
    print(f"  Form: {data.get('form_url', 'NONE')}")
    print()
