with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# scopes を探す
for i, line in enumerate(lines):
    if 'SCOPES' in line or 'scopes' in line:
        for j in range(max(0, i-1), min(i+3, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        print('---')
