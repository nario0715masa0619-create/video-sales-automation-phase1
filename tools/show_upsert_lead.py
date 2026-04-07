with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# upsert_lead 関数を確認
for i, line in enumerate(lines):
    if 'def upsert_lead' in line:
        # 次の50行を表示
        for j in range(i, min(i+50, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
