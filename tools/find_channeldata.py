import os
import glob

# 全ての .py ファイルで ChannelData を検索
for file in glob.glob('*.py'):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'class ChannelData' in line:
            print(f'{file}:{i+1}: {line.rstrip()}')
