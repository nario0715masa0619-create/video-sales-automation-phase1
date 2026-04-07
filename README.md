# 営業自動化プロジェクト - YouTube Data API v3 最適化版

## 📋 プロジェクト概要

YouTube チャンネルから営業リード（企業情報・メールアドレス）を自動収集し、Gemini API でメール生成、SMTP で自動送信するシステム。

**実装期間:** 2026-03-31 ～ 2026-04-07
**プロジェクトステータス:** ✅ 本番環境対応 / Phase 2 開発中

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
- **website_scrape/**: Website クロール結果キャッシュ（新規 - 2026-04-07）

### ✅ 3. リード収集フロー

7ステップフロー: 検索 → 詳細取得 → ICP フィルタリング → 重複排除 → スコアリング → メール抽出 → CRM 更新

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

## 📊 データ収集実績

| 実行日 | ジャンル | チャンネル数 | メール取得数 |
|--------|---------|------------|-----------|
| 2026-04-06 | SNS動画活用 | 74 | 13 |
| 2026-04-07（1回目） | Web制作・デジタル | 49 | 10 |
| **累計** | - | **288** | **50** |

---

## 🔧 改善 3: キャッシング機能（2026-04-07）

### 実装内容
- email_cache.py: キャッシング機能モジュール
- email_extractor.py: キャッシュ読み込み・保存機能

### パフォーマンス
- 改善前: 200チャンネル × 5秒 = 16分
- 改善後: 2回目以降は約20秒（キャッシュから直接読み込み）

### Git コミット
commit: fb45031 / branch: feature/email-extractor-caching

---

## 🔧 セットアップ手順

### 1. 環境変数の設定

.env ファイルを作成:
```\
YOUTUBE_API_KEY=YOUR_KEY
GOOGLE_SHEETS_ID=YOUR_ID
GEMINI_API_KEY=YOUR_KEY
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
```\

### 2. パッケージインストール

```\ash
pip install -r requirements.txt
```\

### 3. Google Sheets 準備

1. YouTube Data API v3 を有効化
2. リード用 Google Sheets を作成
3. config.py の GOOGLE_SHEETS_ID を設定

---

## 📈 使用例

### 基本的な実行
```\ash
python -c "from collect import run_collect; run_collect(dry_run=False)"
```\

### キーワード指定での実行
```\ash
python -c "from collect import run_collect; run_collect(keywords=['Web制作企業', 'Webデザイン企業'], dry_run=False)"
```\

### ドライラン（テスト実行）
```\ash
python -c "from collect import run_collect; run_collect(dry_run=True)"
```\

---

## 🐛 トラブルシューティング

### キャッシュをクリア

```powershell
Remove-Item cache -Recurse -Force
```\

### クォータ不足

- YouTube API は UTC 0:00 にリセット
- config.py の DEFAULT_SEARCH_KEYWORDS を削減
- キャッシュ活用で削減

### メール送信失敗

- .env の SMTP_PASSWORD を確認
- GOOGLE_SHEETS_ID を確認
- GEMINI_API_KEY を確認

---

## 📅 実装タイムライン

| 日付 | タスク | 状態 |
|------|--------|------|
| 2026-03-31 | SerpAPI → YouTube API v3 置換 | ✅ |
| 2026-04-01 | スコアリング統合 | ✅ |
| 2026-04-03 | Phase 1 実装完了 | ✅ |
| 2026-04-07 | キャッシング機能実装 | ✅ |

---

## 🚀 今後の拡張案

1. データベース化: Google Sheets → SQLite
2. メール返信追跡: IMAP で開封検知
3. スケジューリング: Task Scheduler 自動化
4. メール送信自動化: 抽出メールアドレスへの自動送信
5. 問い合わせフォーム自動送信: Selenium で自動入力

---

**最終更新: 2026-04-07 10:45 JST**
**プロジェクトステータス:** ✅ 本番環境対応 / Phase 2 開発中


