with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# upsert_lead が含まれている行を探す
for i, line in enumerate(lines):
    if 'upsert_lead' in line:
        # その前後50行を表示
        start = max(0, i - 50)
        end = min(len(lines), i + 10)
        print('\n'.join([f'{j}: {lines[j].rstrip()}' for j in range(start, end)]))
        print('\n' + '='*80 + '\n')
