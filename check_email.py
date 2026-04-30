with open('website_scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
import re
matches = re.finditer(r"result\['email'\]\s*=\s*(.+)", content)
for match in matches:
    print(f"result['email'] = {match.group(1)}")
