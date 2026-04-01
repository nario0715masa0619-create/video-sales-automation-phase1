with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== collect.py の関数定義 ===')
for i, line in enumerate(lines):
    if line.startswith('def ') or line.startswith('async def '):
        print(f'行 {i+1}: {line.strip()}')
    if 'serpapi' in line.lower() or 'SerpAPI' in line:
        print(f'行 {i+1} [SerpAPI]: {line.strip()[:80]}')
