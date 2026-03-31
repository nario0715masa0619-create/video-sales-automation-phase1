with open('email_sender.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# XserverSMTPSender クラスを探して表示
in_class = False
class_lines = []
for i, line in enumerate(lines):
    if 'class XserverSMTPSender' in line:
        in_class = True
    if in_class:
        class_lines.append((i+1, line.rstrip()))
        # 次のクラス定義か EOF に達したら終了
        if len(class_lines) > 1 and line.startswith('class ') and 'XserverSMTPSender' not in line:
            break
        if len(class_lines) > 50:  # 50 行で打ち切り
            break

print('=== XserverSMTPSender クラス ===')
for line_num, content in class_lines[:40]:
    print(f'{line_num}: {content}')
