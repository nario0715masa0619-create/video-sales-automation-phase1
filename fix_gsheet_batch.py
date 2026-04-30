with open('crm_manager.py','r',encoding='utf-8') as f:
    lines = f.readlines()

# 815 行目（def append_to_gsheet_phase5）を探す
start_line = None
for i, line in enumerate(lines):
    if 'def append_to_gsheet_phase5' in line:
        start_line = i
        break

if start_line is not None:
    # 関数全体を置き換え
    # 815～840 行を削除
    end_line = start_line + 1
    for i in range(start_line + 1, len(lines)):
        if lines[i].strip() and not lines[i][0].isspace():
            end_line = i
            break
        if 'def ' in lines[i] and i > start_line:
            end_line = i
            break
    
    # グローバル変数を追加（ファイルの先頭に）
    new_function = '''def append_to_gsheet_phase5(company_name, phone_number, email, status, website_url):
    """Phase 5 Sheet（別ファイル）にデータを追記 - バッチ処理対応"""
    import time
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            crm = get_crm()
            client = crm._get_client()
            
            # Phase 5 用の別ファイルを開く
            spreadsheet = client.open_by_key(config.SPREADSHEET_ID_PHASE5)
            worksheet = spreadsheet.worksheet(config.SHEET_NAME_PHASE5)
            
            row_data = [
                company_name,
                website_url,
                phone_number,
                email if email else "None",
                "",
                status,
                datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
            ]
            worksheet.append_row(row_data)
            
            logger.info(f"💾 Phase 5 に保存: {company_name} | {phone_number} | {email if email else 'None'} | {status}")
            return True
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 5 * retry_count  # 5秒、10秒、15秒
                logger.warning(f"⚠️  リトライ {retry_count}/{max_retries}: {wait_time} 秒待機")
                time.sleep(wait_time)
            else:
                logger.error(f"❌ Phase 5 保存エラー（最大リトライ回数超過）: {e}")
                return False

'''
    
    # ファイルを再構築
    modified = lines[:start_line] + [new_function + '\n'] + lines[end_line:]
    
    with open('crm_manager.py','w',encoding='utf-8') as f:
        f.writelines(modified)
    
    print('✅ append_to_gsheet_phase5 関数を修正しました')
else:
    print('❌ 関数が見つかりませんでした')
