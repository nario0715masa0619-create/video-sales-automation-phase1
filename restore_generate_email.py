import subprocess

# 33e142f から generate_email 関数を含むセクションを取得
result = subprocess.run(
    ['git', 'show', '33e142f:email_generator.py'],
    capture_output=True,
    text=True,
    encoding='utf-8'
)

if result.returncode != 0:
    print(f'❌ git show エラー: {result.stderr}')
else:
    old_content = result.stdout
    current_content = open('email_generator.py', 'r', encoding='utf-8').read()

    # generate_email 関数を抽出
    import re
    pattern = r'def generate_email\(.*?\).*?(?=\ndef [a-z_]|\Z)'
    match = re.search(pattern, old_content, re.DOTALL)

    if match:
        generate_email_func = match.group(0)
        
        # 現在のファイルに追加
        if 'def generate_email' not in current_content:
            current_content = current_content + '\n\n' + generate_email_func
            
            with open('email_generator.py', 'w', encoding='utf-8') as f:
                f.write(current_content)
            
            print('✅ generate_email 関数を復元しました')
        else:
            print('ℹ️  generate_email 関数は既に存在します')
    else:
        print('❌ generate_email 関数が見つかりません')
