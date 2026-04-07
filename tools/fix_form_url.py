with open("target_scraper.py", "r", encoding="utf-8") as f:
    content = f.read()

# contact_form_url も getattr に変更
content = content.replace(
    "'問い合わせフォームURL': self.contact_form_url,",
    "'問い合わせフォームURL': getattr(self, 'contact_form_url', ''),"
)

with open("target_scraper.py", "w", encoding="utf-8") as f:
    f.write(content)

print("OK")
