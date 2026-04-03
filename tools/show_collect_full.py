with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

print('=== collect.py の全体構成 ===')
print(f'行数: {len(content.split(chr(10)))}')
print(f'ファイルサイズ: {len(content)} 文字')
print()
print('=== インポート部分 ===')
for i, line in enumerate(content.split(chr(10))[:50]):
    if 'import' in line or 'from' in line:
        print(f'{i+1}: {line}')
print()
print('=== run_collect 関数（最初の 80 行）===')
lines = content.split(chr(10))
for i in range(28, min(108, len(lines))):
    print(f'{i+1}: {lines[i]}')
