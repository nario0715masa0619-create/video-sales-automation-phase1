with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== crm_manager.py のメソッド一覧 ===')
for i, line in enumerate(lines):
    if 'def ' in line and not line.strip().startswith('#'):
        print(f'{i+1}: {line.strip()}')

print()
print('=== get_ng_list メソッドの終了行付近 ===')
for i in range(640, min(660, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
