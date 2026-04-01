with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def get_leads_for_email' in line:
        print(f'=== get_leads_for_email（行 {i+1} ～ {min(i+15, len(lines))} ）===')
        for j in range(i, min(i+15, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
