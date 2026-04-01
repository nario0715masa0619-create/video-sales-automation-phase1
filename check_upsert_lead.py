with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def upsert_lead' in line:
        print(f'=== upsert_lead メソッド（行 {i+1} ～ {min(i+70, len(lines))} ）===')
        for j in range(i, min(i+70, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
