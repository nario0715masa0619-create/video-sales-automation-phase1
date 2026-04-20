from crm_manager import CRMManager
from email_extractor import is_valid_email

crm = CRMManager()
all_leads = crm.get_all_leads()

print(f'=== CRM 内のメールアドレス検証 ===')
print(f'総リード数: {len(all_leads)}')

invalid_count = 0
invalid_emails = []

for lead in all_leads:
    email = lead.get('メールアドレス', '')
    if email and email.strip():
        if not is_valid_email(email):
            invalid_count += 1
            ch_name = lead.get('チャンネル名', 'Unknown')
            invalid_emails.append({'channel': ch_name, 'email': email})

print(f'無効なメール: {invalid_count}件')
print(f'\n無効メールアドレス一覧（最初の20件）:')
for item in invalid_emails[:20]:
    print(f"  - {item['channel']}: {item['email']}")
