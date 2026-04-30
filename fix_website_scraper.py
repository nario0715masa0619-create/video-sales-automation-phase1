with open('website_scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# append_phase5_data の呼び出し部分を修正
modified = False
for i in range(len(lines)):
    # result['email'] を None に変更
    if "result['email']" in lines[i] and 'append_phase5_data' in ''.join(lines[max(0, i-5):i+1]):
        lines[i] = lines[i].replace("result['email']", 'None')
        modified = True
        print(f'行 {i+1} を修正: {lines[i].strip()}')

if modified:
    with open('website_scraper.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print()
    print('✅ website_scraper.py を修正しました（CRM メールを None に）')
else:
    print('❌ 修正対象が見つかりませんでした')
