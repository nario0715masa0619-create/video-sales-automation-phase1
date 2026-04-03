with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== JSON 保存部分 ===')
for i, line in enumerate(lines):
    if 'if ch.channel.contact_email:' in line or ('if ch.contact_email:' in line):
        for j in range(max(0, i-1), min(i+8, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
