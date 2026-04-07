with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# upsert_lead 関数の全体を表示
for i, line in enumerate(lines):
    if 'def upsert_lead' in line:
        # 関数の最後（次のdef までか、またはクラス終了まで）を表示
        for j in range(i, min(i+100, len(lines))):
            print(f'{j+1:4d}: {lines[j].rstrip()}')
            # 次のdef が見つかったら終了
            if j > i and 'def ' in lines[j] and j > i+10:
                break
        break
