with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# filter_by_icp 関数を探す
import re
match = re.search(r'def filter_by_icp\(.*?\):(.*?)(?=\ndef |\nclass |\Z)', content, re.DOTALL)
if match:
    func_def = 'def filter_by_icp' + match.group(0)[len('def filter_by_icp'):]
    lines = func_def.split('\n')[:40]  # 最初の40行
    for i, line in enumerate(lines):
        print(f'{i+1}: {line}')
else:
    print('filter_by_icp 関数が見つかりません')
