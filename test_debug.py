from tools.website_crawler import crawl_domain
from tools.email_extractor import extract_email
import re
from bs4 import BeautifulSoup

url = "https://pepacomi.com"
html_list = crawl_domain(url, max_pages=1)

html = html_list[0]

# 正規表現で直接検索
pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
matches = re.findall(pattern, html)

print(f"正規表現マッチ数: {len(matches)}")
for match in matches[:10]:
    print(f"  - {match}")

# mailto リンク検索
soup = BeautifulSoup(html, 'html.parser')
mailto_links = soup.find_all('a', href=re.compile(r'^mailto:'))
print(f"\nmailto リンク数: {len(mailto_links)}")
for link in mailto_links[:5]:
    print(f"  - {link.get('href')}")
