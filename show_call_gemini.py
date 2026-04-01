with open('email_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def _call_gemini' in line:
        print(f'=== _call_gemini 関数（行 {i+1} ～ {min(i+20, len(lines))} ）===')
        for j in range(i, min(i+20, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
