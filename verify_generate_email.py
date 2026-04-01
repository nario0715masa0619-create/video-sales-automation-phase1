with open('email_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'def generate_email' in content:
    print('✅ generate_email 関数は存在します')
    
    # 行番号を表示
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def generate_email' in line:
            print(f'行 {i+1}: {line}')
else:
    print('❌ generate_email 関数は見つかりません')
