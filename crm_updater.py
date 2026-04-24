import logging
import sys
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/phase6_crm_updater.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# config.py から設定を読込
try:
    from config import SPREADSHEET_ID_PHASE5, SHEET_NAME_PHASE5, CRM_SPREADSHEET_ID, CRM_SHEET_NAME
except ImportError:
    logger.error("config.py が見つかりません")
    sys.exit(1)

def get_google_sheets_client():
    """Google Sheets クライアントを取得"""
    try:
        creds = Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        return gspread.authorize(creds)
    except FileNotFoundError:
        logger.error("credentials.json が見つかりません")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Google Sheets クライアント作成エラー: {e}")
        sys.exit(1)

def read_phase5_emails():
    """Phase 5 Sheet からメールアドレスを読込"""
    try:
        client = get_google_sheets_client()
        sheet = client.open_by_key(SPREADSHEET_ID_PHASE5)
        worksheet = sheet.worksheet(SHEET_NAME_PHASE5)
        
        rows = worksheet.get_all_values()
        email_data = []
        
        for idx, row in enumerate(rows[1:], start=2):
            if len(row) < 4:
                continue
            
            company_name = row[0].strip() if row[0] else ""
            website_url = row[1].strip() if row[1] else ""
            email = row[3].strip() if len(row) > 3 else ""
            
            if company_name and website_url and email and email != "None":
                email_data.append({
                    'row_idx': idx,
                    'company_name': company_name,
                    'website_url': website_url,
                    'email': email
                })
        
        logger.info(f"Phase 5 から {len(email_data)} 件のメールアドレスを読込")
        return email_data
    except Exception as e:
        logger.error(f"Phase 5 読込エラー: {e}")
        sys.exit(1)

def read_crm_leads():
    """CRM Sheet "Leads" から全行を読込"""
    try:
        client = get_google_sheets_client()
        sheet = client.open_by_key(CRM_SPREADSHEET_ID)
        worksheet = sheet.worksheet(CRM_SHEET_NAME)
        
        rows = worksheet.get_all_values()
        crm_data = []
        
        for idx, row in enumerate(rows[1:], start=2):
            if len(row) < 3:
                continue
            
            company_name = row[0].strip() if row[0] else ""
            website_url = row[1].strip() if len(row) > 1 and row[1] else ""
            current_email = row[2].strip() if len(row) > 2 else ""
            
            send_count = 0
            if len(row) > 25:
                try:
                    send_count = int(row[25]) if row[25] else 0
                except ValueError:
                    send_count = 0
            
            if company_name and website_url:
                crm_data.append({
                    'row_idx': idx,
                    'company_name': company_name,
                    'website_url': website_url,
                    'current_email': current_email,
                    'send_count': send_count
                })
        
        logger.info(f"CRM Leads から {len(crm_data)} 件を読込")
        return crm_data, worksheet
    except Exception as e:
        logger.error(f"CRM 読込エラー: {e}")
        sys.exit(1)



def match_and_update(phase5_emails, crm_data, worksheet):
    """メールアドレスを上書き"""
    updated_list = []
    skipped_list = []
    error_list = []
    
    for phase5 in phase5_emails:
        p5_company = phase5['company_name']
        p5_url = phase5['website_url']
        p5_email = phase5['email']
        
        matched = False
        for crm in crm_data:
            if crm['company_name'] == p5_company and crm['website_url'] == p5_url:
                matched = True
                current_email = crm['current_email']
                crm_row_idx = crm['row_idx']
                send_count = crm['send_count']
                
                try:
                    worksheet.update_cell(crm_row_idx, 3, p5_email)
                    logger.info(f"✅ 上書き: {p5_company} | {p5_url} | {current_email} → {p5_email}")
                    
                    updated_list.append({
                        'company_name': p5_company,
                        'website_url': p5_url,
                        'old_email': current_email,
                        'new_email': p5_email,
                        'row_idx': crm_row_idx,
                        'send_count': send_count
                    })
                except Exception as e:
                    logger.error(f"❌ 上書きエラー: {p5_company} | {e}")
                    error_list.append(p5_company)
                
                break
        
        if not matched:
            logger.warning(f"⏭️  一致する企業なし: {p5_company} | {p5_url}")
            skipped_list.append({
                'company_name': p5_company,
                'website_url': p5_url
            })
    
    return updated_list, skipped_list, error_list

def reset_send_history(updated_list, worksheet):
    """送信履歴をリセット（Z>0 の場合）"""
    reset_count = 0
    reset_error_count = 0
    
    for updated in updated_list:
        send_count = updated['send_count']
        crm_row_idx = updated['row_idx']
        company_name = updated['company_name']
        website_url = updated['website_url']
        
        if send_count > 0:
            try:
                worksheet.update_cell(crm_row_idx, 26, 0)
                
                for col in range(27, 32):
                    worksheet.update_cell(crm_row_idx, col, "")
                
                logger.info(f"✅ リセット: {company_name} | {website_url} | Z: {send_count} → 0, AA～AE: クリア")
                reset_count += 1
            except Exception as e:
                logger.error(f"❌ リセットエラー: {company_name} | {e}")
                reset_error_count += 1
    
    return reset_count, reset_error_count



def main():
    """Phase 6 メイン処理"""
    logger.info("=" * 80)
    logger.info("Phase 6 CRM メールアドレス更新 & 送信履歴リセット開始")
    logger.info("=" * 80)
    
    start_time = datetime.now()
    
    # Phase 5 からメールアドレスを読込
    phase5_emails = read_phase5_emails()
    
    if not phase5_emails:
        logger.warning("Phase 5 に有効なメールアドレスがありません")
        return
    
    # CRM Leads を読込
    crm_data, worksheet = read_crm_leads()
    
    if not crm_data:
        logger.warning("CRM Leads にデータがありません")
        return
    
    # メールアドレスを上書き
    updated_list, skipped_list, error_list = match_and_update(phase5_emails, crm_data, worksheet)
    
    # 送信履歴をリセット（Z>0 の場合）
    reset_count, reset_error_count = reset_send_history(updated_list, worksheet)
    
    # 統計出力
    total = len(updated_list) + len(skipped_list) + len(error_list)
    elapsed = (datetime.now() - start_time).total_seconds()
    
    logger.info("=" * 80)
    logger.info(f"処理完了: {total} 件")
    logger.info(f"  ✅ 上書き: {len(updated_list)} 件")
    
    reset_only = len(updated_list) - reset_count
    logger.info(f"    → うち リセット: {reset_count} 件（Z>0 だった企業）")
    logger.info(f"    → うち 上書きのみ: {reset_only} 件（Z=0 のまま）")
    
    logger.info(f"  ⏭️  スキップ: {len(skipped_list)} 件（一致なし）")
    logger.info(f"  ❌ エラー: {len(error_list)} 件")
    
    if reset_error_count > 0:
        logger.warning(f"  ⚠️  リセット失敗: {reset_error_count} 件")
    
    logger.info(f"実行時間: {elapsed:.1f} 秒")
    logger.info("=" * 80)

if __name__ == '__main__':
    main()

