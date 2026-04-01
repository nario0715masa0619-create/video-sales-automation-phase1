with open('email_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== email_generator.py の関数定義 ===')
for i, line in enumerate(lines):
    if line.startswith('def ') and not line.startswith('    def'):
        print(f'{i+1}: {line.rstrip()}')

print('\n=== __all__ の定義 ===')
for i, line in enumerate(lines):
    if '__all__' in line:
        for j in range(i, min(i+10, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
else:
    print('__all__ が定義されていません')
