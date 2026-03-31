with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# CRMManager クラスの最後のメソッドを探す
in_class = False
last_method_line = -1
last_method_name = ''

for i, line in enumerate(lines):
    if 'class CRMManager' in line:
        in_class = True
    
    if in_class and line.startswith('    def '):
        last_method_line = i
        last_method_name = line.strip()
    
    if in_class and line.startswith('class ') and 'CRMManager' not in line:
        break

print(f'最後のメソッド: 行 {last_method_line+1}')
print(f'メソッド名: {last_method_name}')
print()
print('=== 最後のメソッド周辺（行 {}-{} ） ==='.format(max(1, last_method_line-5), min(len(lines), last_method_line+20)))
for i in range(max(0, last_method_line-5), min(len(lines), last_method_line+20)):
    print(f'{i+1}: {lines[i].rstrip()}')
