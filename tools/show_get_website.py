with open('email_extractor.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# get_website_from_youtube 関数全体を表示
for i, line in enumerate(lines):
    if 'def get_website_from_youtube' in line:
        for j in range(i, min(i+40, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
