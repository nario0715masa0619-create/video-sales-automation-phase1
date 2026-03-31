with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'unique_channels = {ch.channel.channel_url: ch for ch in channels}' in content:
    print('✅ コードは存在します')
    
    # その部分を表示
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'unique_channels' in line:
            for j in range(max(0, i-2), min(len(lines), i+5)):
                print(f'{j+1}: {lines[j]}')
            break
else:
    print('❌ コードが存在しません')
