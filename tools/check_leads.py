from crm_manager import read_website_urls_from_crm
leads = read_website_urls_from_crm(limit=10)
for idx, (row_idx, url, email, company) in enumerate(leads, 1):
    status = email if email else "[空]"
    print(f'{idx}. {company} | {status}')
