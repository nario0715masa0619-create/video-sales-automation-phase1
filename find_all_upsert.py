with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# upsert_lead がどこで呼ばれているか全て確認
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'upsert_lead' in line:
        print(f'{i}: {line}')
