with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# to_crm_dict の戻り値を確認
for i, line in enumerate(lines):
    if 'def to_crm_dict' in line:
        # 次の30行を表示
        for j in range(i, min(i+30, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
