with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# upsert_lead 関数の「update_values」部分を探す
in_update = False
for i, line in enumerate(lines):
    if 'update_values' in line and i > 240:  # upsert_lead内での最初の update_values
        in_update = True
    if in_update:
        print(f'{i+1:4d}: {lines[i].rstrip()}')
        if 'self.sheet.update' in line:  # 最初の sheet.update を見つけたら終了
            for j in range(i+1, min(i+10, len(lines))):
                print(f'{j+1:4d}: {lines[j].rstrip()}')
            break
