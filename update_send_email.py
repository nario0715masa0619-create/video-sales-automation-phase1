import re

with open('send_email.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
for i, line in enumerate(lines):
    output.append(line)
    if 'crm.update_after_email_send(lead_dict, success=True)' in line:
        indent = len(line) - len(line.lstrip())
        output.append(' ' * indent + '# メール送信回数をインクリメント\n')
        output.append(' ' * indent + 'current_count = int(lead_dict.get(\"メール送信回数\", 0) or 0)\n')
        output.append(' ' * indent + 'lead_dict[\"メール送信回数\"] = current_count + 1\n')

with open('send_email.py', 'w', encoding='utf-8') as f:
    f.writelines(output)

print('メール送信回数 インクリメント追加完了')
