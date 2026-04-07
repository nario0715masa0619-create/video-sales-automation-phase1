with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 行 41-50 を確認
print('=== collect.py のキーワード部分（行 40-52） ===')
for i in range(39, min(52, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
