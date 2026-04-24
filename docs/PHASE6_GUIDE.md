# Phase 6 実装ガイド

## 概要

Phase 6 は Phase 5 で抽出したメールアドレスを CRM Sheet "Leads" に反映し、既営業企業の送信履歴をリセットするパイプラインです。

## アーキテクチャ図

Google Sheet Phase 5（866 行）
  ├─ Column A: company_name
  ├─ Column B: website_url
  └─ Column D: email
    ↓
crm_updater.py
  ├─ read_phase5_emails()
  ├─ read_crm_leads()
  ├─ match_and_update()
  ├─ reset_send_history()
  └─ log_statistics()
    ↓
CRM Sheet "Leads"
  ├─ Column C: email（上書き完了）
  ├─ Column Z: メール送信回数（リセット対象）
  └─ Column AA～AE: 送信日時（クリア対象）
    ↓
既存パイプライン（daily_operations.py）
  ├─ send_email.py が Column Z == 0 を検知
  └─ 新しいメールアドレスへ自動送信開始
    ↓
logs/phase6_crm_updater.log（処理ログ）

## crm_updater.py 関数リファレンス

### get_google_sheets_client()

入力: なし
処理: credentials.json から Google Sheets API クライアントを作成
出力: gspread.Spreadsheet オブジェクト
例外: FileNotFoundError（credentials.json が見つからない）

### read_phase5_emails()

入力: なし
処理:
  1. Google Sheet Phase 5 を開く
  2. SPREADSHEET_ID_PHASE5, SHEET_NAME_PHASE5 から config.py を読込
  3. 全行を読込、ヘッダをスキップ
  4. Column A（company_name）、Column B（website_url）、Column D（email）を抽出
  5. email != "None" の行のみを対象
  6. リストを返す

出力: 
[
  {
    'row_idx': 2,
    'company_name': '企業 A',
    'website_url': 'https://example.com',
    'email': 'contact@example.com'
  },
  ...
]

例外: FileNotFoundError, gspread.exceptions.SpreadsheetNotFound

### read_crm_leads()

入力: なし
処理:
  1. Google Sheet CRM を開く
  2. CRM_SPREADSHEET_ID, CRM_SHEET_NAME="Leads" から config.py を読込
  3. 全行を読込、ヘッダをスキップ
  4. Column A～C, Z, AA～AE を抽出
  5. company_name と website_url がある行のみを対象

出力:
(
  [
    {
      'row_idx': 2,
      'company_name': '企業 A',
      'website_url': 'https://example.com',
      'current_email': 'old@example.com',
      'send_count': 3,
      'send_dates': ['2026-01-01 10:00:00', '2026-01-08 10:00:00', '2026-01-15 10:00:00']
    },
    ...
  ],
  all_rows  # 全行データ（更新用）
)

例外: FileNotFoundError, gspread.exceptions.SpreadsheetNotFound

### match_and_update(phase5_emails, crm_data, worksheet)

入力:
  phase5_emails: read_phase5_emails() の出力
  crm_data: read_crm_leads() の出力[0]
  worksheet: CRM Sheet worksheet オブジェクト

処理:
  1. 各 Phase 5 行について、company_name + website_url で CRM を検索
  2. 一致する行があれば、Column C（3 列目）にメールアドレスを上書き
  3. worksheet.update_cell(row_idx, 3, email) を実行
  4. 成功 / スキップ / エラーをログ出力

出力:
(
  updated_list: list,  # 更新成功した企業リスト
  skipped_list: list,  # スキップした企業リスト（一致なし）
  error_list: list     # エラーが発生した企業リスト
)

例外: gspread.exceptions.APIError（Google Sheets API エラー）

### reset_send_history(updated_list, crm_data, worksheet)

入力:
  updated_list: match_and_update() の出力の updated_list
  crm_data: read_crm_leads() の出力[0]
  worksheet: CRM Sheet worksheet オブジェクト

処理:
  1. updated_list の各企業について、Column Z を確認
  2. Column Z > 0（既営業）の場合のみ処理
  3. Column Z を 0 にリセット（worksheet.update_cell(row_idx, 26, 0)）
  4. Column AA～AE（26～30 列）をクリア
     worksheet.update_cell(row_idx, col, "") for col in [27, 28, 29, 30, 31]
  5. リセット成功 / 失敗をログ出力

出力:
(
  reset_count: int,  # リセット成功件数
  reset_error_count: int  # リセット失敗件数
)

例外: gspread.exceptions.APIError（Google Sheets API エラー）

### main()

入力: なし
処理:
  1. ログ初期化
  2. Phase 5 データ読込
  3. CRM Leads データ読込
  4. メールアドレス上書き
  5. 送信履歴リセット（Z>0 の場合）
  6. 統計ログ出力

出力: なし（ログファイルに出力）

## 設定項目（config.py）

SPREADSHEET_ID_PHASE5: Phase 5 Google Sheet ID
SHEET_NAME_PHASE5: Phase 5 Sheet 名
CRM_SPREADSHEET_ID: CRM Google Sheet ID
CRM_SHEET_NAME: CRM Sheet 名（"Leads" で固定）

## ログ設定

ログレベル: INFO
ログファイル: logs/phase6_crm_updater.log
ログ形式: %(asctime)s - %(levelname)s - %(message)s
出力先: ファイル（UTF-8）+ コンソール

## 実行フロー（疑似コード）

start_time = datetime.now()
logger.info("Phase 6 CRM メールアドレス更新 & 送信履歴リセット開始")

phase5_emails = read_phase5_emails()
# 出力: "Phase 5 から X 件のメールアドレスを読込"

crm_data, worksheet = read_crm_leads()
# 出力: "CRM Leads から Y 件を読込"

updated_list, skipped_list, error_list = match_and_update(phase5_emails, crm_data, worksheet)
# 出力: 各行の上書き / スキップ / エラー

reset_count, reset_error = reset_send_history(updated_list, crm_data, worksheet)
# 出力: リセット成功 / 失敗件数

elapsed = (datetime.now() - start_time).total_seconds()
logger.info(f"処理完了: {len(updated_list) + len(skipped_list) + len(error_list)} 件")
logger.info(f"  ✅ 上書き: {len(updated_list)} 件")
logger.info(f"    → うち リセット: {reset_count} 件")
logger.info(f"  ⏭️  スキップ: {len(skipped_list)} 件（一致なし）")
logger.info(f"  ❌ エラー: {len(error_list)} 件")
logger.info(f"実行時間: {elapsed:.1f} 秒")



## トラブルシューティング

### credentials.json not found

症状: FileNotFoundError が出力される

対応:
1. Google Cloud Console で OAuth 2.0 credentials を作成
2. credentials.json をダウンロード
3. プロジェクト root に配置
4. python crm_updater.py で再実行

### Sheet not found

症状: gspread.exceptions.SpreadsheetNotFound が出力される

対応:
1. config.py で SPREADSHEET_ID_PHASE5, CRM_SPREADSHEET_ID を確認
2. Google Sheet のリンクから ID を確認
3. config.py を修正
4. python crm_updater.py で再実行

### Access Denied

症状: 403 Forbidden エラー

対応:
1. service account email（credentials.json に記載）を確認
2. Google Sheet の共有設定で service account を追加
3. 読み書き権限を付与
4. python crm_updater.py で再実行

### Network Error

症状: 接続タイムアウト、接続拒否

対応:
1. インターネット接続を確認
2. Google Sheets API が有効か Google Cloud Console で確認
3. ファイアウォール設定を確認
4. python crm_updater.py で再実行

## 実行コマンド

### 基本実行

python crm_updater.py

### ログ確認

Get-Content logs/phase6_crm_updater.log -Tail 50

### 統計確認

Get-Content logs/phase6_crm_updater.log | Select-String "処理完了|上書き|スキップ|エラー|リセット"

## パフォーマンス

### 実行時間の内訳

Phase 5 読込: 1～2 秒（866 行）
CRM Leads 読込: 1～2 秒（1705 行）
マッチング & 上書き: 2～3 秒
送信履歴リセット: 1～2 秒
合計: 5～10 秒（推定）

### ネットワーク遅延の影響

Google Sheets API は遅延が 1～2 秒/リクエスト
大量リセットの場合は batch update の導入を検討

## 実行例

### 実行コマンド

PS D:\...\video-sales-automation-phase1> python crm_updater.py

### 出力例

2026-04-24 15:30:00 - INFO - ================================================================================
2026-04-24 15:30:00 - INFO - Phase 6 CRM メールアドレス更新 & 送信履歴リセット開始
2026-04-24 15:30:00 - INFO - ================================================================================
2026-04-24 15:30:01 - INFO - Phase 5 から 45 件のメールアドレスを読込
2026-04-24 15:30:02 - INFO - CRM Leads から 1705 件を読込
2026-04-24 15:30:02 - INFO - ✅ 上書き: 企業 A | https://example.com |  → contact@example.com
2026-04-24 15:30:03 - INFO - ✅ リセット: 企業 B | https://sample.jp | Z: 3 → 0, AA～AE: クリア
2026-04-24 15:30:04 - INFO - ✅ 上書き（リセットなし）: 企業 C | https://test.jp |  → info@test.jp (Z=0)
2026-04-24 15:30:05 - INFO - ⏭️  一致する企業なし: 企業 D | https://other.com
2026-04-24 15:30:06 - INFO - ⏭️  一致する企業なし: 企業 E | https://another.jp
2026-04-24 15:30:07 - INFO - ================================================================================
2026-04-24 15:30:07 - INFO - 処理完了: 45 件
2026-04-24 15:30:07 - INFO -   ✅ 上書き: 40 件
2026-04-24 15:30:07 - INFO -     → うち リセット: 25 件（Z>0 だった企業）
2026-04-24 15:30:07 - INFO -     → うち 上書きのみ: 15 件（Z=0 のまま）
2026-04-24 15:30:07 - INFO -   ⏭️  スキップ: 5 件（一致なし）
2026-04-24 15:30:07 - INFO -   ❌ エラー: 0 件
2026-04-24 15:30:07 - INFO - 実行時間: 7.5 秒
2026-04-24 15:30:07 - INFO - ================================================================================

## メール送信フロー（Phase 6 実行後）

### 既存パイプラインとの連携

1. Phase 6 実行
   - CRM Sheet Column C: 新しいメールアドレスに上書き
   - CRM Sheet Column Z: 0 にリセット
   - CRM Sheet Column AA～AE: クリア

2. daily_operations.py 実行（定時）
   - send_email.py を呼び出し
   - get_pending_leads() で対象リードを抽出

3. get_pending_leads() の処理
   - 抽出条件：Column Z == 0（未接触）
   - Phase 6 でリセットされた企業が自動的に抽出される

4. send_email.py が新しいメールアドレスへ自動送信

### 完全な営業サイクル

Phase 5 抽出 → Phase 6 反映 & リセット → daily_operations（自動メール送信）
    ↓
新しいメールアドレスに対する営業活動が自動的に開始される

## 注意事項

### 上書きは不可逆

CRM Sheet に上書きされたメールアドレスは復元できません。事前に backup を取るか、テストで動作確認してください。

### マッチング精度

company_name と website_url が完全に一致する必要があります。スペースやドメイン形式が異なる場合はマッチしません。

### 送信履歴はクリア不可逆

Column Z と AA～AE をクリアすると、送信履歴が失われます。重要な場合は CRM Sheet を backup してください。

### リセット対象の確認

Phase 6 実行前に、以下を確認してください：
- CRM Sheet でリセットされる企業を特定
- Column Z > 0 の企業数を確認
- 必要に応じて CRM Sheet を backup

## 依存ライブラリインストール

pip install gspread google-auth-oauthlib google-auth-httplib2

