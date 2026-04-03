with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# クラス定義とメソッドを探す
for i, line in enumerate(lines):
    if 'class ' in line or 'def ' in line:
        print(f'{i+1:4d}: {line.rstrip()}')
