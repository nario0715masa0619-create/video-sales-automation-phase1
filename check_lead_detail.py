from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

if leads:
    first_lead = leads[0]
    print('最初のリードの全カラム:')
    for key, value in first_lead.items():
        print(f'  {key}: {value}')
