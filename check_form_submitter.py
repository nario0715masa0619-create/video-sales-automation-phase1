with open('form_submitter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== form_submitter.py のクラス定義 ===')
for i, line in enumerate(lines):
    if 'class ' in line:
        print(f'{i+1}: {line.rstrip()}')

print('\n=== 関数定義 ===')
for i, line in enumerate(lines):
    if line.startswith('def ') and not line.startswith('    def'):
        print(f'{i+1}: {line.rstrip()}')
