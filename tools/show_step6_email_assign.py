with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 ループのメール割り当て部分を表示
print('=== Step 6 メール割り当て部分 ===')
for i, line in enumerate(lines):
    if 'email_data_loop' in line and 'contact_email' in line:
        for j in range(max(0, i-1), min(i+4, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
