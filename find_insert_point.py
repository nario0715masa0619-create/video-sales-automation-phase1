with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# get_ng_list メソッドの終了位置を探す
method_start = 601  # 行 602（0 ベース）
method_end = method_start + 1

# メソッドの終了を探す（インデント < 4 の行まで）
for i in range(method_start + 1, len(lines)):
    line = lines[i]
    # 空行はスキップ
    if line.strip() == '':
        continue
    # インデントが 4 未満 = メソッドの終了
    if line.startswith('    ') and not line.startswith('        '):
        # 次のメソッドの開始
        method_end = i
        break
    # インデントが 0-3 = クラスの終了
    if not line.startswith('    '):
        method_end = i
        break
else:
    # ループを抜けた = ファイルの末尾
    method_end = len(lines)

print(f'get_ng_list メソッド: 行 {method_start+1} ～ {method_end}')
print(f'挿入位置: 行 {method_end}')
print()
print('=== 挿入位置周辺 ===')
for i in range(max(0, method_end-5), min(len(lines), method_end+5)):
    print(f'{i+1}: {lines[i].rstrip()}')
