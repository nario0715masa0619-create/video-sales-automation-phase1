with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# print_quota_status を呼び出している行を探す
print('=== print_quota_status の呼び出し ===')
for i, line in enumerate(lines):
    if 'print_quota_status' in line:
        for j in range(max(0, i-2), min(i+3, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        print('---')
