from tools.website_crawler import crawl_domain

url = "https://pepacomi.com"
result = crawl_domain(url, max_pages=5)

print(f"取得した HTML 数: {len(result)}")
for i, html in enumerate(result, 1):
    print(f"  {i}. {len(html)} bytes")
