with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def update_after_email_send' in line:
        print(f'=== update_after_email_send メソッド（行 {i+1} ～ {min(i+20, len(lines))} ）===')
        for j in range(i, min(i+20, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
