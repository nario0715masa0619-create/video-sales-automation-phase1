# crm_manager.py を手動で修復
with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 290行目付近を確認して表示
print('=== 280-300行目の確認 ===')
for i in range(279, min(300, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
