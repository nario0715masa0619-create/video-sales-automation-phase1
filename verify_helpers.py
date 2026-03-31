with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'def get_leads_for_email' in content:
    print('✅ get_leads_for_email が存在します')
else:
    print('❌ get_leads_for_email が存在しません')
    
if 'def get_leads_for_form' in content:
    print('✅ get_leads_for_form が存在します')
else:
    print('❌ get_leads_for_form が存在しません')
