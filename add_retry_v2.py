# email_generator.py にリトライロジックを追加

with open('email_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# genai.GenerativeModel を使っている行を探す
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # genai.GenerativeModel の呼び出しを検出
    if 'model = genai.GenerativeModel(' in line:
        # 以降の3行（model定義とresponse生成）を置換
        if i + 2 < len(lines) and 'response = model.generate_content(prompt)' in lines[i+2]:
            # インデント取得
            indent = len(line) - len(line.lstrip())
            spaces = ' ' * indent
            
            # 新しいコード（リトライ付き）に置換
            new_lines.append(f'{spaces}# ResourceExhausted エラーにリトライ対応\n')
            new_lines.append(f'{spaces}@retry(\n')
            new_lines.append(f'{spaces}    stop=stop_after_attempt(3),\n')
            new_lines.append(f'{spaces}    wait=wait_exponential(multiplier=2, min=5, max=60),\n')
            new_lines.append(f'{spaces}    retry=retry_if_exception_type((Exception,)),\n')
            new_lines.append(f'{spaces}    reraise=True\n')
            new_lines.append(f'{spaces})\n')
            new_lines.append(f'{spaces}def _call_api():\n')
            new_lines.append(f'{spaces}    model = genai.GenerativeModel(\n')
            new_lines.append(f'{spaces}        model_name=config.GEMINI_MODEL,\n')
            new_lines.append(f'{spaces}    )\n')
            new_lines.append(f'{spaces}    response = model.generate_content(prompt)\n')
            new_lines.append(f'{spaces}    return response.text.strip()\n')
            new_lines.append(f'{spaces}return _call_api()\n')
            
            # 元の3行をスキップ
            i += 3
            continue
    
    new_lines.append(line)
    i += 1

with open('email_generator.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ リトライロジック追加完了')
