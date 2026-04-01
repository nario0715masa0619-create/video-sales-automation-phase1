with open('send_email.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== update_after_email_send の呼び出し ===')
for i, line in enumerate(lines):
    if 'update_after_email_send' in line:
        for j in range(max(0, i-3), min(len(lines), i+3)):
            print(f'{j+1}: {lines[j].rstrip()}')
        print()
