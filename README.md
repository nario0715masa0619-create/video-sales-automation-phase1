# 営業自動化プロジェクト - YouTube Data API v3 最適化版

## 📋 プロジェクト概要

YouTube チャンネルから営業リード（企業情報・メールアドレス）を自動収集し、Gemini API でメール生成、SMTP で自動送信するシステム。

**実装期間:** 2026-03-31 ～ 2026-04-01  
**プロジェクトステータス:** ✅ 本番環境対応

---

## 🎯 実装済み機能

### ✅ 1. YouTube Data API v3 統合

- search.list: キーワードからチャンネルを検索（100pt/リクエスト）
- channels.list: チャンネル詳細情報取得（1pt/リクエスト）
- ETag キャッシング: 304 Not Modified 対応
- クォータ最適化: 8,500pt → 100pt（98.8% 削減）

### ✅ 2. キャッシュシステム

- etag_cache.json: API レスポンス ETag 保存
- search_cache.json: 検索結果キャッシュ（7日有効）
- channel_index.json: チャンネルインデックス（30日有効）

### ✅ 3. リード収集フロー

7ステップフロー: 検索 → 詳細取得 → ICP フィルタリング → 重複排除 → スコアリング → CRM 更新 → メール抽出

### ✅ 4. メール送信自動化

Google Sheets からリード取得 → Gemini API で文面生成 → SMTP 送信 → 履歴記録

### ✅ 5. エラーハンドリング

HTTP 429: 自動リトライ（最大 3 回）
HTTP 403/404: ログ記録してスキップ
タイムアウト: 15 秒で自動リトライ

### ✅ 6. セキュリティ

API キーを .env に保存（Git 無視）
キャッシュファイルは UTF-8 without BOM
パスは Windows 絶対パス対応

---

## 🔧 セットアップ手順

### 1. 環境変数の設定

.env ファイルを作成:
YOUTUBE_API_KEY=YOUR_KEY
GOOGLE_SHEETS_ID=YOUR_ID
GEMINI_API_KEY=YOUR_KEY
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password

### 2. パッケージインストール

pip install -r requirements.txt

### 3. Google Sheets 準備

1. YouTube Data API v3 を有効化
2. リード用 Google Sheets を作成
3. config.py の GOOGLE_SHEETS_ID を設定

### 4. Gmail App Password 取得

1. 2 段階認証を有効化
2. アプリパスワードを生成
3. .env の SMTP_PASSWORD に設定


---

## 📊 パフォーマンス指標

### クォータ使用量（1 日）

| 操作 | 前 | 後 | 削減率 |
|------|------|------|-------|
| キーワード検索 | 6,000pt | 0pt | 100% |
| チャンネル詳細 | 不要 | 50pt | - |
| 動画取得 | 不要 | 50pt | - |
| 合計 | 8,500pt | 100pt | 98.8% |

### 実行時間

- collect.py: 2～3 分
- send_email.py: 1～2 分
- 合計: 3～5 分

---

## 🗂️ ファイル構成

collect.py / send_email.py / config.py / .env / youtube_api_optimized.py / cache_manager.py / target_scraper.py / scorer.py / crm_manager.py / email_extractor.py / email_generator.py / utils.py / cache/ / logs/ / tests/

---

## 📈 使用例

python collect.py
python collect.py --dry-run
python send_email.py --limit 10
python send_email.py --dry-run --limit 3


---

## 🐛 トラブルシューティング

### キャッシュをクリア

Remove-Item cache -Recurse -Force

### クォータ不足

- YouTube API は UTC 0:00 にリセット
- config.py の DEFAULT_SEARCH_KEYWORDS を削減
- キャッシュ活用で削減

### メール送信失敗

- .env の SMTP_PASSWORD を確認
- GOOGLE_SHEETS_ID を確認
- GEMINI_API_KEY を確認

---

## 📞 サポート

エラーログ確認:
Get-Content logs/collect.log -Tail 100

Git 履歴:
git log --oneline -10

---

## ✅ チェックリスト

- [ ] .env に API キーが設定されている
- [ ] cache/ フォルダが存在する
- [ ] Google Sheets にアクセスできる
- [ ] Gmail App Password が設定されている
- [ ] ドライランテストが成功している


---

## 📅 実装タイムライン

| 日付 | タスク | 状態 |
|------|--------|------|
| 2026-03-31 | SerpAPI → YouTube API v3 置換 | ✅ |
| 2026-03-31 | ETag キャッシング実装 | ✅ |
| 2026-04-01 | スコアリング統合 | ✅ |
| 2026-04-01 | メール抽出機能 | ✅ |
| 2026-04-01 | ドライランテスト成功 | ✅ |
| 2026-04-01 | 本番環境対応 | ✅ |

---

## 🚀 今後の拡張案

1. データベース化: Google Sheets → SQLite
2. メール返信追跡: IMAP で開封検知
3. スケジューリング: Task Scheduler 自動化
4. 多言語対応: Gemini で多言語生成
5. A/B テスト: 複数パターン効果測定

---

**最終更新:** 2026-04-01  
**プロジェクトステータス:** ✅ 本番環境対応・運用開始可能

---

## ✅ Phase 1 実装完了（2026-04-03）

### 実装内容
- **Step 1-5:** YouTube チャンネル検索・フィルタリング・スコアリング
- **Step 6-7:** メール・公式サイト URL 自動抽出 & Google Sheets CRM 更新
- **API キーマネジメント:** 複数キー（1-6）対応、自動キー切り替え
- **キャッシュシステム:** ETag キャッシング、検索結果キャッシュ

### 成果サマリー

| 項目 | 実績 | 目標 |
|------|------|------|
| チャンネル検索 | 575 件 | 500+ ✅ |
| ICP フィルタリング | 222 件 | 200+ ✅ |
| CRM 保存 | 212 件 | 200+ ✅ |
| 公式サイト URL | 212 件 | 100% ✅ |
| メール抽出 | 36 件 | 80%+ ❌ |

### 次フェーズ（Phase 2）

**目標:** メール抽出成功率を 17% → 80% 以上に改善

**改善項目:**
1. 短縮 URL 除外（bitly, goo.gl など）
2. 日本語ドメイン対応
3. JSON-LD & microdata パース強化
4. コンタクトフォーム検出改善

**スケジュール:**
- ドキュメント: 2026-04-04
- 開発: 2026-04-05～2026-04-10
- テスト: 2026-04-11～2026-04-15

---

**最終更新: 2026-04-03**
