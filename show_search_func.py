with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# search_company_channels 関数を探す
in_func = False
func_lines = []
for i, line in enumerate(lines):
    if 'def search_company_channels' in line:
        in_func = True
    if in_func:
        func_lines.append((i+1, line.rstrip()))
        if line.strip().startswith('return ') and in_func:
            # return 文まで抽出
            for j in range(max(0, len(func_lines)-20), len(func_lines)):
                print(f'{func_lines[j][0]}: {func_lines[j][1]}')
            break

if not func_lines:
    print('関数が見つかりません')
