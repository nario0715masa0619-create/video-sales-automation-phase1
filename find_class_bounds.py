with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# CRMManager クラスの定義を探す
class_start = None
class_end = None
for i, line in enumerate(lines):
    if 'class CRMManager' in line:
        class_start = i
    if class_start is not None and i > class_start and line.startswith('class '):
        class_end = i
        break

if class_start is None:
    print('CRMManager クラスが見つかりません')
else:
    if class_end is None:
        # ファイルの末尾がクラス
        class_end = len(lines)
    
    print(f'CRMManager クラス: 行 {class_start+1} ～ {class_end}')
    
    # クラス内の最後のメソッドを探す
    last_method_line = class_start
    for i in range(class_start, class_end):
        if lines[i].startswith('    def '):
            last_method_line = i
    
    print(f'最後のメソッド: 行 {last_method_line+1}')
    print(f'追加位置: 行 {last_method_line+1} ～ {class_end}')
