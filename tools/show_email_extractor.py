with open('email_extractor.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== email_extractor.py の関数一覧 ===')
for i, line in enumerate(lines):
    if line.startswith('def '):
        print(f'{i+1}: {line.strip()}')

print()
print('=== 最初の 50 行 ===')
for i in range(min(50, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
