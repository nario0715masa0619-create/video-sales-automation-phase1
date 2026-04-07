with open('email_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def _build_email_1' in line:
        print(f'=== 修正後の _build_email_1 ===')
        for j in range(i, min(i+50, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
