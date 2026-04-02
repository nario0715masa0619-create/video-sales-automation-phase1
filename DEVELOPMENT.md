# DEVELOPMENT.md - 開発ガイド & デグレード防止

## 目次
1. プロジェクト構造
2. Step 6 と Step 7 の依存関係（重要）
3. コード変更時のチェックリスト
4. テスト実行方法
5. デグレード事例と対策

---

## 1. プロジェクト構造

ビデオ営業自動化プロジェクト：
- collect.py: メインスクリプト（リード収集）
- send_email.py: メール送信スクリプト
- config.py: 設定ファイル
- target_scraper.py: YouTube チャンネルデータ抽出
- crm_manager.py: Google Sheets 連携
- email_extractor.py: メールアドレス抽出
- scorer.py: スコアリングロジック
- utils.py: ユーティリティ関数
- youtube_api_optimized.py: YouTube Data API v3
- cache_manager.py: キャッシュ管理
- CHECKLIST.md: コミット前チェックリスト
- DEVELOPMENT.md: このファイル
- README.md: プロジェクト概要
- cache/: キャッシュディレクトリ
- logs/: ログディレクトリ
- tests/: テストディレクトリ

---

## 2. Step 6 と Step 7 の依存関係（重要）

### なぜこれが重要なのか？

2026-04-02 のデグレードで、Step 6 と Step 7 の順序が逆になり、メール情報が Google Sheets に保存されなくなった問題が発生しました。

### 正しい実行順序

Step 7: メールアドレス抽出
→ ch.contact_email = email
→ ch.contact_form_url = contact_form_url
↓
Step 6: CRM 更新
→ lead_data = ch.to_crm_dict() （メール情報を含む）
↓
Google Sheets に保存

### 間違った順序（デグレードの原因）

Step 6: CRM 更新
→ lead_data = ch.to_crm_dict() （メール情報がまだ空）
↓
Google Sheets に保存（メールなし）
↓
Step 7: メールアドレス抽出
→ ch.contact_email = email （既に Step 6 が完了しているので反映されない）

### collect.py での実装確認

Step 7 のコード（107-129行目）：
Step 7: メールアドレス抽出
for i, ch in enumerate(scored_channels):
    try:
        website_url, email, contact_form_url = extractor.extract_email(channel_url)
        ch.contact_email = email if email else '' （重要）
        ch.contact_form_url = contact_form_url if contact_form_url else '' （重要）

Step 6 のコード（132-145行目）：
Step 6: CRM 更新
for i, ch in enumerate(scored_channels):
    try:
        lead_data = ch.to_crm_dict() （メール情報を含む）
        upsert_lead(lead_data)

---

## 3. コード変更時のチェックリスト

### Step 6 または Step 7 を変更する場合

必ず以下を確認してください：

1. Step の順序確認
   - collect.py で Step 7 が Step 6 より前にあるか

2. メール設定確認
   - ch.contact_email = email が実行されているか
   - ch.contact_form_url = contact_form_url が実行されているか

3. to_crm_dict() 確認
   - target_scraper.py の to_crm_dict() にメール情報が含まれているか

4. upsert_lead() 確認
   - crm_manager.py の upsert_lead() が メールアドレス と お問い合わせフォームURL を処理しているか

---

## 4. テスト実行方法

### ユニットテスト（Step 6/7 の依存関係を検証）

python -m pytest tests/test_collect_integration.py -v

期待される出力：
test_collect_integration.py::TestCollectIntegration::test_channel_data_has_email_fields PASSED
test_collect_integration.py::TestCollectIntegration::test_step7_sets_contact_email_before_step6 PASSED

### ドライラン（エラーなく実行できるか）

python collect.py --dry-run --keywords テストキーワード

確認項目：
- エラーが出ていない
- メール取得成功 が複数表示
- CRM データ検証 エラーが出ていない

### 本番実行（メール情報が実際に保存されているか）

Remove-Item cache -Recurse -Force -ErrorAction SilentlyContinue
python collect.py

確認スクリプト：
from crm_manager import CRMManager
crm = CRMManager()
leads = crm.get_all_leads()
print(f'総リード数: {len(leads)} 件')
with_email = sum(1 for lead in leads if lead.get('メールアドレス'))
print(f'メール情報あり: {with_email} 件')
print(f'比率: {with_email/len(leads)*100:.1f}%')
if with_email / len(leads) >= 0.8:
    print('✅ メール情報が正常に保存されています')
else:
    print('❌ メール情報の保存比率が低い')

---

## 5. デグレード事例と対策

### 2026-04-02 のデグレード

症状：Google Sheets にメールアドレスが保存されない

原因：コミット 9a32169 で Step 7 の実装が変更され、以下の処理が削除された：
- ch.contact_email = email if email else ''
- ch.contact_form_url = contact_form_url if contact_form_url else ''

発見方法：ドライラン後、Google Sheets のメール件数が 0 件だった

修正方法：
1. Step 7 → Step 6 の順序を確認
2. Step 7 で ch.contact_email を設定する処理を復元
3. テストとドライランで検証
4. コミット：fix: correct Step 6/7 order and add email validation

### 再発防止

1. 自動検証 - collect.py の最後に validate_crm_data_saved() を実行
2. ユニットテスト - Step 6/7 の依存関係をテスト
3. チェックリスト - コミット前に CHECKLIST.md を確認
4. ドキュメント - このファイルで Step 6/7 の重要性を記載

---

## コミットガイドライン

### Step 6 または Step 7 を変更する場合

コミットメッセージ例：
fix: correct Step 6/7 order - email data must be set before CRM update
- Step 7 (email extraction) now comes before Step 6 (CRM update)
- Added ch.contact_email and ch.contact_form_url assignment
- Added validate_crm_data_saved() check at end of collect.py
- Updated tests in test_collect_integration.py

コミット前に実行すべきコマンド：
1. python -m pytest tests/test_collect_integration.py -v
2. python collect.py --dry-run --keywords テスト
3. Remove-Item cache -Recurse -Force -ErrorAction SilentlyContinue
4. python collect.py
5. メール情報確認スクリプト実行

---

## トラブルシューティング

### メール情報が保存されていない

1. collect.py の Step 順序確認
   - Step 7 が Step 6 より前にあるか確認

2. ch.contact_email 設定の確認
   - collect.py に ch.contact_email = email が存在するか確認

3. target_scraper.py の to_crm_dict() 確認
   - メールアドレス: self.contact_email が含まれているか確認

### テストが失敗する

python -m pytest tests/test_collect_integration.py -v --tb=short

詳細なエラーメッセージを確認してトラブルシューティング

---

## 参考資料

- CHECKLIST.md: コミット前検証チェックリスト
- README.md: プロジェクト概要
- tests/test_collect_integration.py: 自動テスト
- utils.py: validate_crm_data_saved() 関数

最終更新: 2026-04-02
ステータス: デグレード防止機構完成
