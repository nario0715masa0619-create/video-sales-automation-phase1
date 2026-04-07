with open('email_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# generate_email 関数を探す
for i, line in enumerate(lines):
    if 'def generate_email' in line:
        print(f'=== generate_email 関数（行 {i+1} ～ {min(i+50, len(lines))} ）===')
        for j in range(i, min(i+50, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
