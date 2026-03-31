with open('scorer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# score_channels 関数全体を表示
in_func = False
indent_level = 0
for i, line in enumerate(lines):
    if 'def score_channels' in line:
        in_func = True
        indent_level = len(line) - len(line.lstrip())
        start_line = i
    
    if in_func:
        current_indent = len(line) - len(line.lstrip())
        if i > start_line and line.strip() and current_indent <= indent_level and not line.strip().startswith('#'):
            break
        print(f'{i+1}: {line.rstrip()}')
