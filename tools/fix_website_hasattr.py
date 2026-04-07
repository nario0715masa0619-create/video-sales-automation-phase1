with open("target_scraper.py", "r", encoding="utf-8") as f:
    content = f.read()

# hasattr チェックを getattr に変更
content = content.replace(
    "'公式サイト': self.website_url if hasattr(self, 'website_url') else '',",
    "'公式サイト': getattr(self, 'website_url', ''),"
)

with open("target_scraper.py", "w", encoding="utf-8") as f:
    f.write(content)

print("OK")
