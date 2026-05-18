import re

with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# update_after_email_send を探して修正
if 'def update_after_email_send' in content:
    # 最終送信日の設定後に、メール送信回数を追加
    old = "lead['最終送信日'] = datetime.now().isoformat()\n        else:"
    new = "lead['最終送信日'] = datetime.now().isoformat()\n            current_count = int(lead.get('メール送信回数', 0) or 0)\n            lead['メール送信回数'] = current_count + 1\n        else:"
    
    content = content.replace(old, new)
    
    with open('crm_manager.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('修正完了')
else:
    print('update_after_email_send が見つかりません')
