with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== crm_manager.py 最後の 30 行 ===')
for i in range(max(0, len(lines)-30), len(lines)):
    print(f'{i+1}: {lines[i].rstrip()}')
