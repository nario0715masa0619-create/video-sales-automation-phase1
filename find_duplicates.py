from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

# チャンネルURL の重複を検出
from collections import Counter
urls = [l.get('チャンネルURL', '') for l in leads if l.get('チャンネルURL')]
url_counts = Counter(urls)
duplicates = {url: count for url, count in url_counts.items() if count > 1}

print(f'総リード数: {len(leads)}')
print(f'ユニークなチャンネルURL: {len(url_counts)}')
print(f'重複しているURL: {len(duplicates)}件')

if duplicates:
    print('\n重複URLの例（上位10件）:')
    for url, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f'  {url}: {count}回')
