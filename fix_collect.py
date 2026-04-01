with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 行 51-52 を修正（SerpAPI キーの使用を削除）
new_lines = []
for i, line in enumerate(lines):
    # 行 50-52 の SerpAPI キー取得と呼び出しを削除
    if i == 50:  # 行 51（0ベース）
        continue  # SerpAPI キー行をスキップ
    elif i == 51:  # 行 52
        # search_company_channels の呼び出しを修正
        new_lines.append('        urls = search_company_channels(keyword)\n')
    else:
        new_lines.append(line)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ collect.py を修正しました（SerpAPI キー削除）')
