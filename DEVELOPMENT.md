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


## 7. API キーフェイルオーバー（KEY 1-6 対応）

**背景**: YouTube Data API v3 のクォータが枯渇したり、単一キーが 403 エラーを返す場合に対応するため、複数の API キー（1-6）をサポート。

**実装詳細:**
- youtube_api_optimized.py で KEY 1-6 対応を実装
- .env に最大 6 つのキーを設定可能
- 403 エラー発生時に自動的に KEY 1 → KEY 2 → ... → KEY 6 に順番に切り替え
- キー別のクレジット使用状況を追跡

**設定方法（.env）:**
`env
YOUTUBE_API_KEY1=your_api_key_1
YOUTUBE_API_KEY2=your_api_key_2
YOUTUBE_API_KEY3=your_api_key_3
YOUTUBE_API_KEY4=your_api_key_4
YOUTUBE_API_KEY5=your_api_key_5
YOUTUBE_API_KEY6=your_api_key_6
`

**動作フロー:**
1. KEY 1 で実行開始
2. 403 Forbidden エラー → KEY 2 に自動切り替え
3. KEY 2 も失敗 → KEY 3, 4, 5, 6 と順番に試行
4. すべてのキーが失敗 → エラーログ出力

**ログ出力例:**
`
API キーを切り替えました (キー 1/6 → 2/6)
別の API キーで再試行します [search:YouTube活用]
検索完了: 12 件 (API KEY 2, クォータ消費: 100 pt)
`

**キー別クレジット追跡:**
`bash
# get_quota_status() で各キーのクレジット使用状況を確認
KEY 1: 8,000 pt 使用
KEY 2: 2,500 pt 使用
KEY 3: 未使用
KEY 4: 未使用
KEY 5: 未使用
KEY 6: 未使用
`

**テスト:**
`bash
python -m pytest tests/test_api_fallback.py -v
`

テスト項目:
- test_multiple_api_keys_loaded: KEY 1-6 が読み込まれるか
- test_api_key_fallback_on_403: 403 エラー時にキーが切り替わるか
- test_fallback_order: KEY 1 → 2 → 3... の順番で試行されるか
- test_fallback_fails_when_all_keys_exhausted: 全キー無効時に False を返すか

**参考ファイル:**
- youtube_api_optimized.py: API キーフェイルオーバー実装（KEY 1-6 対応）
- config.py: YOUTUBE_API_KEY1～6 設定管理
- tests/test_api_fallback.py: ユニットテスト

---
## Phase 1 完了 & Phase 2 計画（2026-04-03）

### Phase 1 実装完了

**チェック済み項目:**
- ✅ YouTube 検索・詳細取得
- ✅ ICP フィルタリング & スコアリング
- ✅ メール & URL 自動抽出
- ✅ Google Sheets CRM 連携
- ✅ API キーフェイルオーバー（KEY 1-6）
   - youtube_api_optimized.py で KEY 1-6 対応実装
   - 403 エラー時に自動キー切り替え
   - キー別クレジット追跡機能
- ✅ キャッシュシステム
- ✅ エラーハンドリング & リトライ
- ✅ テストモード廃止

**実績:**
- チャンネル検索: 575 件
- ICP フィルタリング: 222 件
- CRM 保存: 212 件
- 公式サイト URL: 100%
- メール抽出: 36 件（17%）

### Phase 2 開発予定

**目標:** メール抽出成功率を 17% → 80%+ に改善

**改善項目:**

1. **短縮 URL 除外**
   - bitly, goo.gl, tinyurl, short.link など
   - EXCLUDE_DOMAINS に追加

2. **日本語ドメイン対応**
   - .jp, .co.jp ドメイン対応
   - 新しい regex パターン追加

3. **JSON-LD & microdata 強化**
   - 既存: 基本的な JSON-LD パース
   - 改善: 完全な microdata サポート、schema.org 対応

4. **コンタクトフォーム検出改善**
   - 候補パス拡張（"contact", "お問い合わせ", "お知らせ" など）
   - キーワードマッチング精度向上

5. **メール正規表現パターン拡張**
   - 既存: 基本的なメールパターン
   - 改善: 複雑なメール形式対応

**スケジュール:**
- 計画・ドキュメント: 2026-04-04
- 実装: 2026-04-05～2026-04-10
- テスト: 2026-04-11～2026-04-15
- デプロイ: 2026-04-16

**テスト方法:**
\\\ash
# email_extractor.py の改善版をテスト
python email_extractor.py <channel_url>

# 目標: 80% 以上のメール取得成功率
\\\

---

**最終更新: 2026-04-03**




