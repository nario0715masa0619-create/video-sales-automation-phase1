with open('email_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# _build_email_1 関数を探す
for i, line in enumerate(lines):
    if 'def _build_email_1' in line:
        print(f'=== _build_email_1 関数（行 {i+1} ～ {min(i+40, len(lines))} ）===')
        for j in range(i, min(i+40, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
