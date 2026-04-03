with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# print_quota_status() の呼び出しを全て削除
content = content.replace('    print_quota_status()\n', '')
content = content.replace('        print_quota_status()\n', '')

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ print_quota_status() の呼び出しを削除しました')
