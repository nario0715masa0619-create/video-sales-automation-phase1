with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 7 の終了位置を探す
import re
step7_match = re.search(r'(=== Step 7.*?(?===|$))', content, re.DOTALL)

if step7_match:
    step7_text = step7_match.group(1)
    # 最後の100行を表示
    lines = step7_text.split('\n')
    print('=== Step 7 の最後の20行 ===')
    for line in lines[-20:]:
        print(line)
else:
    print('Step 7 が見つかりません')
