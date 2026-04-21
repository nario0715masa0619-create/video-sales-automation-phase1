# Implementation Checklist - Video Sales Automation Phase 1

## Phase 1: Core Implementation

### Step 1: バウンスチェック (bounce_checker.py)
- [x] IMAP ログイン機能
- [x] バウンスメール検出
- [x] ログ記録
- [x] 日次スケジュール実行

### Step 2: メール送信 (send_email.py)
- [x] メール生成（Gemini API）
- [x] SMTP 送信
- [x] 送信履歴ログ（SQLite）
- [x] 初回/リピート分離ロジック ✅ NEW (2026-04-21)
- [x] リピート不足補填ロジック ✅ NEW (2026-04-21)
- [x] dry-run モード
- [x] 時間制限（23:00 停止）
- [x] 送信間隔制御（ランダム遅延）

### Step 3: Lead 収集 (collect.py)
- [x] YouTube API で動画検索
- [x] チャンネル詳細情報取得
- [x] ICP フィルタリング
- [x] スコアリング（A/B/C ランク）
- [x] CRM に upsert
- [x] Step 6a: メールアドレス抽出 (email_extractor.py)
- [ ] Step 6b: フォーム自動送信 (未実装、Phase 2 延期)
- [x] Step 7: CRM 更新

### Step 4: バウンス管理
- [x] バウンス検出
- [x] バウンスフラグ設定
- [x] 送信対象から除外

### Step 5: スケジュール管理
- [x] Windows タスクスケジューラ登録
- [x] 毎日 09:00 自動実行
- [x] ログファイル出力

## 設計・仕様書

### email_extractor.py
- [x] 仕様書作成 (email_extractor_SPECIFICATION.md)
- [x] HTML 変数参照順序バグ修正 ✅ NEW (2026-04-21)
- [x] 戻り値統一（3 値）
- [x] ドキュメント整備

### Step 6b（フォーム自動送信）
- [x] 実装延期決定
- [x] 延期理由をドキュメント化 (STEP6B_IMPLEMENTATION_SUSPENSION.md)
- [x] contact_form_extractor.py をコメントアウト
- [ ] Phase 2 で実装予定

### daily_operations.py
- [x] argparse で引数処理対応 ✅ NEW (2026-04-21)
- [x] --dry-run フラグ追加
- [x] --limit パラメータ対応

## テスト・動作確認

### Step 1: バウンスチェック
- [x] IMAP 接続テスト
- [x] バウンス検出ロジック
- [x] ログ出力確認

### Step 2: メール送信
- [x] Gemini API メール生成テスト
- [x] SMTP 送信テスト
- [x] 初回送信テスト（10 件）
- [x] 初回/リピート分離テスト ✅ NEW (2026-04-21)
- [x] リピート補填ロジックテスト ✅ NEW (2026-04-21)
- [x] dry-run で 15 件メール生成確認 ✅ NEW (2026-04-21)
- [ ] 本番実行テスト（2026-04-22 予定）

### Step 3: Lead 収集
- [x] YouTube API テスト
- [x] チャンネル詳細情報取得テスト
- [x] ICP フィルタテスト
- [x] スコアリングテスト
- [x] CRM upsert テスト
- [x] メール抽出テスト（email_extractor）
- [ ] Form 送信テスト（未実装）

### Step 4: バウンス管理
- [x] バウンス検出テスト
- [x] フラグ設定テスト

### Step 5: スケジュール
- [x] タスクスケジューラ登録確認
- [ ] 自動実行ログ確認（2026-04-22 予定）

## バグ修正・改善

### 2026-04-21
- [x] email_extractor.py: HTML 変数参照順序バグ修正
- [x] send_email.py: 初回/リピート分離ロジック追加
- [x] send_email.py: リピート補填ロジック追加
- [x] daily_operations.py: argparse 対応
- [x] daily_operations.py: --dry-run フラグ追加

### 2026-04-20
- [x] db_manager.py: interval_days 条件修正（行 107）

### 2026-04-18
- [x] collect.py: Step 6b をコメントアウト

### 2026-04-17
- [x] email_extractor.py 仕様書作成

## Git コミット履歴

| 日付 | コミット | 内容 |
|------|---------|------|
| 2026-04-21 | TBD | send_email.py 初回/リピート分離、補填ロジック実装 |
| 2026-04-21 | 0299222 | Step 6b コメントアウト、email_extractor 仕様書追加 |
| 2026-04-20 | 99d2c1a | db_manager.py interval_days 修正 |
| 2026-04-18 | (multiple) | collect.py Step 6 修正 |
| 2026-04-17 | d7e795d | PHONE_EXTRACTION_DESIGN.md 作成 |
| 2026-04-17 | ff2e5e1 | リポジトリ整理 |

## 本番環境への展開

### 準備完了
- [x] 初回/リピート分離ロジック実装
- [x] dry-run で動作確認
- [x] ドキュメント更新
- [x] Git コミット

### 本番実行予定
- [ ] 2026-04-22 09:00 スケジュール自動実行（DailyEmailOperations）
- [ ] 送信ログ確認
- [ ] CRM メール送信回数更新確認
- [ ] 問題なければ運用継続

## 今後の課題

### Phase 2
1. Step 6b フォーム自動送信実装
   - contact_form_extractor.py の完全性確認
   - 実運用テスト（Google Forms、Formspree など）
   - エラーハンドリング強化

2. collect.py メール抽出率向上（20% → 50%）
   - email_extractor.py の精度改善
   - 追加パターンマッチング
   - キャッシュ戦略最適化

3. リプライ率計測
   - 返信メール自動分類
   - リプライ率レポート生成
   - AI による自動返信提案

### 保留事項
- interval_days テスト値（0）を本番値（3）に戻す手順書作成
- CRM の email 抽出率 20% → 50% への改善計画
- リポジトリのドキュメント整備（TROUBLESHOOTING.md など）
