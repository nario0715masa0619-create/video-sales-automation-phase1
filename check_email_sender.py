with open('email_sender.py', 'r', encoding='utf-8') as f:
    content = f.read()

print('=== email_sender.py の内容確認 ===')
print(content[:1000])  # 最初の 1000 文字を表示
print('\n...\n')

# クラス定義を探す
import re
classes = re.findall(r'class \w+.*?:', content)
print(f'定義されているクラス: {classes}')

# SMTP 関連を検索
if 'smtplib' in content:
    print('✅ smtplib をインポート')
else:
    print('❌ smtplib をインポートしていない')

if 'Xserver' in content or 'xserver' in content.lower():
    print('✅ Xserver 関連の記述あり')
else:
    print('❌ Xserver 関連の記述なし')
