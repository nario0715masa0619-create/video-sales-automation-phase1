with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 6 直前のメール情報読込部分を表示
for i, line in enumerate(lines):
    if 'メール情報をロード' in line or 'email_data.json' in line:
        for j in range(max(0, i-2), min(i+15, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        print('---')
