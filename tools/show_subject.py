with open('email_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def _build_email_1' in line:
        print(f'=== _build_email_1 の subject 部分（行 {i+1} ～ {min(i+15, len(lines))} ）===')
        for j in range(i, min(i+15, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
