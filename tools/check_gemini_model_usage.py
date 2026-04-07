with open('email_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== email_generator.py で使用されているモデル ===')
for i, line in enumerate(lines):
    if 'GenerativeModel' in line or 'genai.generate' in line or 'model =' in line:
        if 'gemini' in line.lower():
            print(f'{i+1}: {line.rstrip()}')
