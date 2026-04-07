from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

print(f"Total leads: {len(leads)}")
print()

for i, lead in enumerate(leads):
    email = lead.get("メールアドレス", "NONE")
    name = lead.get("会社名", "NO_NAME")
    print(f"{i+1}. {name}: email={email}")
