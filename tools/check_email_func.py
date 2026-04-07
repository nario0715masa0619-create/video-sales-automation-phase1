with open('email_extractor.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def get_email_from_youtube_channel' in line:
        for j in range(i, min(i+30, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
        break
