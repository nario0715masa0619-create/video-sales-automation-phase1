with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ChannelData クラスを探す
for i, line in enumerate(lines):
    if 'class ChannelData' in line:
        # クラス定義の最初の30行を表示
        for j in range(i, min(i+30, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
