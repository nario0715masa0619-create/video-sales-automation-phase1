with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# upsert_lead 関数を探す
for i, line in enumerate(lines):
    if 'def upsert_lead' in line:
        start = i
        end = min(len(lines), i + 80)
        print(f'=== upsert_lead 関数 (行 {start+1}-{end+1}) ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
