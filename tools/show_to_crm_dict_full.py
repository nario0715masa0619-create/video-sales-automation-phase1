with open('target_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# to_crm_dict() の return 以下を表示
for i, line in enumerate(lines):
    if 'def to_crm_dict' in line:
        # return から閉じ括弧まで表示
        for j in range(i, min(i+60, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
            if '}' in lines[j] and j > i+2:
                break
        break
