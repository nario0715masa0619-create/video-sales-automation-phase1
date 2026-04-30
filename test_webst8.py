from tools.website_crawler import crawl_domain
from tools.email_extractor import extract_email

url = "https://webst8.com"
html_list = crawl_domain(url, max_pages=5)

print(f"取得した HTML 数: {len(html_list)}")

for i, html in enumerate(html_list, 1):
    email = extract_email(html)
    print(f"  {i}. email: {email}")
