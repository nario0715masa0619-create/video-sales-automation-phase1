# Phase 6 実装計画書

## 概要

Phase 6 は Phase 5 で抽出したメールアドレスを CRM Sheet "Leads" に反映し、既営業企業の送信履歴をリセットして再営業対象にするパイプラインです。

## ミッション

Phase 5 Google Sheet から抽出したメールアドレスを CRM Sheet "Leads" Column C に上書きし、既に送信済みの企業の場合は送信履歴をリセットします。

## 入力

### データソース

Google Sheet Phase 5（Phase 5 で生成）
- Sheet Name: （config.SHEET_NAME_PHASE5）
- Column A: company_name（企業名）
- Column B: website_url（ウェブサイト URL）
- Column D: email（メールアドレス）

### データ件数

- 総行数: 866 件（ヘッダ除く）
- 有効メール: 約 45～100 件（推定、Phase 5 に依存）

## CRM Sheet "Leads" の列定義

| 列 | 定義 | 説明 |
|---|---|---|
| A | company_name | 企業名 |
| B | website_url | ウェブサイト URL |
| C | メールアドレス | 連絡先メール（Phase 6 で上書き） |
| Z | メール送信回数 | 送信履歴カウント（0=未送信、1～n=送信済み） |
| AA | 1 回目送信日時 | YYYY-MM-DD HH:MM:SS |
| AB | 2 回目送信日時 | YYYY-MM-DD HH:MM:SS |
| AC | 3 回目送信日時 | YYYY-MM-DD HH:MM:SS |
| AD | 4 回目送信日時 | YYYY-MM-DD HH:MM:SS |
| AE | 5 回目送信日時 | YYYY-MM-DD HH:MM:SS |

## 処理フロー

### ステップ 1: Phase 5 データ読込

- Google Sheet Phase 5 の全行を読込
- Column A（company_name）、Column B（website_url）、Column D（email）を抽出
- 条件：email != "None" の行のみを対象

### ステップ 2: CRM Leads データ読込

- CRM Sheet "Leads" の全行を読込
- Column A（company_name）、Column B（website_url）、Column C（email）、Column Z（メール送信回数）を抽出

### ステップ 3: マッチング & メールアドレス上書き

各 Phase 5 行について：
1. company_name + website_url の組合せで CRM Leads を検索
2. 一致する行があれば、Column C にメールアドレスを上書き

### ステップ 4: 送信履歴リセット判定

上書き後、Column Z の値を確認：

IF Column Z == 0:
  Y（未営業）→ 処理終了、何もしない
ELSE (Column Z > 0):
  N（既営業）→ ステップ 5 へ

### ステップ 5: 送信履歴のクリア（再営業対象にする）

既営業企業の場合、以下をクリア：
- Column Z（メール送信回数）を 0 にリセット
- Column AA～AE（全 5 回の送信日時）をクリア

結果：新しいメールアドレスから改めてメール送信が開始される

### ステップ 6: ログ & 統計

- 上書き件数、スキップ件数、エラー件数、リセット件数をログ出力
- logs/phase6_crm_updater.log に記録

## 出力

### 更新結果

CRM Sheet "Leads" が以下のように更新されます：

| company_name | website_url | メール（更新前） | メール（更新後） | Z（回数） | AA～AE（送信日時） |
|---|---|---|---|---|---|
| 企業 A | https://example.com | （空） | contact@example.com | 0 | （空） |
| 企業 B | https://sample.jp | old@sample.jp | new@sample.jp | 0（リセット） | （すべてクリア） |

### ログファイル

Path: logs/phase6_crm_updater.log

内容:
- 処理開始時刻
- 読込件数（Phase 5、CRM Leads）
- 上書き件数、スキップ件数、エラー件数、リセット件数
- 各行の更新内容
  - 上書きのみ（Z=0 のまま）
  - 上書き + リセット（Z>0 から Z=0 にリセット）
  - スキップ（一致なし）
- 処理終了時刻、実行時間

## マッチングロジック

### 一致条件

Phase 5 の (company_name, website_url)
    ↓
CRM Leads を検索
    ↓
company_name が完全一致 AND website_url が完全一致
    ↓
YES: 上書き & 履歴リセット判定
NO: スキップ

### 上書き & リセットルール

Step 1: Column C をメールアドレスで上書き
  CRM.Leads[row, C] = Phase 5.email

Step 2: Column Z を確認
  IF Z == 0 (未営業):
    何もしない（処理終了）
  ELSE (Z > 0, 既営業):
    Column Z を 0 にリセット
    Column AA～AE をすべてクリア



## 実装要件

### 必須設定（config.py）

SPREADSHEET_ID_PHASE5 = "..."
SHEET_NAME_PHASE5 = "..."
CRM_SPREADSHEET_ID = "..."
CRM_SHEET_NAME = "Leads"

### 必須ファイル

- credentials.json（Google Sheets API 認証）
- config.py（設定値）
- crm_updater.py（Phase 6 メインスクリプト）
- logs/ フォルダ（ログ出力先）

### 依存ライブラリ

- gspread
- google-auth-oauthlib
- google-auth-httplib2

## 実行方法

### 手動実行

python crm_updater.py

### 実行時間

- 読込: 1～2 秒（Phase 5: 866 行、CRM: 1705 行）
- マッチング & 更新: 3～5 秒
- 合計: 5～10 秒（推定）

## 既存パイプラインとの連携

### 自動メール送信フロー

Phase 6 実行後、既存の daily_operations.py が以下のフローで自動的にメール送信を開始します：

1. Phase 6 で Column Z がリセット（0）される
2. daily_operations.py（定時実行）が send_email.py を実行
3. send_email.py が get_pending_leads() で対象リードを抽出
4. Column Z == 0 の企業が自動的に抽出される
5. 新しいメールアドレスへメール送信開始

※ 追加実装は不要。Phase 6 で Column Z をリセットするだけで、既存パイプラインが自動的に対応します。

## エラーハンドリング

### 予想される例外

credentials.json not found: Google Sheets API 認証失敗
Sheet not found: Phase 5 または CRM Sheet が見つからない
Access Denied: Google Sheet へのアクセス権がない
Network Error: ネットワーク接続失敗

### 対応

- すべてのエラーを logs/phase6_crm_updater.log に記録
- エラーが発生した行はスキップして続行
- 最終統計で成功 / スキップ / エラー件数を表示

## テスト計画

### テストケース 1: 基本動作（未営業企業）

- Phase 5 に 3 件のメールアドレスを準備
- CRM で一致する企業を 3 件準備（Z=0）
- 実行: python crm_updater.py
- 期待:
  - 3 件のメールアドレスを上書き
  - Z はそのまま 0
  - AA～AE はクリアされない
  - ログ: "3 件上書き（リセットなし）"

### テストケース 2: 既営業企業のリセット

- Phase 5 に 2 件のメールアドレスを準備
- CRM で一致する企業を 2 件準備（Z=3, AA～AC に日時あり）
- 実行: python crm_updater.py
- 期待:
  - 2 件のメールアドレスを上書き
  - Z を 3 から 0 にリセット
  - AA～AE をすべてクリア
  - ログ: "2 件上書き（2 件リセット）"

### テストケース 3: 混合（一部未営業、一部既営業）

- Phase 5 に 5 件のメールアドレスを準備
- CRM で一致する企業を 5 件準備（Z=0 が 2 件、Z>0 が 3 件）
- 実行: python crm_updater.py
- 期待:
  - 5 件すべてを上書き
  - Z=0 の 2 件はそのまま
  - Z>0 の 3 件をリセット
  - ログ: "5 件上書き（3 件リセット）"

### テストケース 4: 一致なし

- Phase 5 に 2 件のメールアドレスを準備
- CRM に該当企業が存在しない
- 実行: python crm_updater.py
- 期待:
  - スキップ：2 件
  - ログ: "2 件スキップ（一致なし）"

### テストケース 5: email が "None"

- Phase 5 に email="None" の行がある
- 実行: python crm_updater.py
- 期待:
  - Phase 5 読込時にフィルタリング
  - email="None" の行は処理対象外
  - ログに含まれない

## 注意事項

### 上書きは不可逆

CRM Sheet に上書きされたメールアドレスは復元できません。事前に backup を取るか、テストで動作確認してください。

### マッチング精度

company_name と website_url が完全に一致する必要があります。スペースやドメイン形式が異なる場合はマッチしません。

### 送信履歴はクリア不可逆

Column Z と AA～AE をクリアすると、送信履歴が失われます。重要な場合は CRM Sheet を backup してください。

## 今後の拡張

- マッチング精度向上（部分一致、ドメイン抽出など）
- 更新前データの backup 自動作成
- メール検証機能（SMTP 確認など）

