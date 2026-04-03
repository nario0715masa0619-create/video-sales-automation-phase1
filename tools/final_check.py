from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

print(f"Total leads: {len(leads)}")
print()

for i, lead in enumerate(leads):
    email = lead.get("メールアドレス", "")
    website = lead.get("公式サイト", "")
    form = lead.get("問い合わせフォームURL", "")
    name = lead.get("会社名", "NO_NAME")
    print(f"{i+1}. {name}")
    print(f"   Email: {email if email else 'EMPTY'}")
    print(f"   Website: {website if website else 'EMPTY'}")
    print(f"   Form: {form if form else 'EMPTY'}")
    print()
