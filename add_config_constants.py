with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 定数を追加
new_constants = '''
# メール/フォーム送信設定
EMAIL_MAX_SEND_PER_RUN = 10
FORM_MAX_SEND_PER_RUN = 5
'''

if 'EMAIL_MAX_SEND_PER_RUN' not in content:
    content = content.rstrip() + '\n' + new_constants + '\n'
    
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ config.py に定数を追加しました')
else:
    print('ℹ️  既に定数が存在します')
