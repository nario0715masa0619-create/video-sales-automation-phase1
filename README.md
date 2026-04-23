# Video Sales Automation - Phase 1

## プロジェクト概要
YouTube チャンネル向けの営業自動化プロジェクト。
日次で lead を収集し、メール送信を自動化します。

## 最終更新
- 日時: 2026-04-21 22:32
- バージョン: v1.0.0
- ステータス: Phase 1 運用中

## 主要機能

### Step 1: バウンスチェック (bounce_checker.py)
- IMAP でメールボックスをスキャン
- バウンスメール（エラー）を検出・ログ記録
- 自動的に「バウンスフラグ」を CRM に反映

### Step 2: メール送信 (send_email.py)
- 初回メール: 候補の 70% を 1 通目で送信
- リピート: 候補の 30% を 3 日以上経過後に 2 通目で送信
- リピート不足時: 初回で補填（常に daily_limit 件を送信）
- 送信間隔: 1200 秒 ± 50% のランダム間隔
- 23:00 に自動停止（JSTC 営業時間外）

## 設計・仕様書

### email_extractor.py
- 目的: YouTube チャンネルから公式サイト URL → メールアドレスを抽出
- 機能: 
  - yt-dlp で About URL を取得
  - BeautifulSoup で HTML をスクレイピング
  - JSON-LD、mailto:、正規表現で多段階抽出
  - 成功率: 40% → 80% に改善
- 詳細: email_extractor_SPECIFICATION.md 参照

### Step 6b（フォーム自動送信）
- 現状: 未実装（Phase 2 対応予定）
- 理由: contact_form_extractor.py は実装完了だが、実運用テスト不足
- 詳細: STEP6B_IMPLEMENTATION_SUSPENSION.md 参照

## システム構成

### コアスクリプト（ルート）
- daily_operations.py - 日次運用のオーケストレーション
- bounce_checker.py - バウンスメールチェック
- send_email.py - メール送信エンジン
- collect.py - lead 収集パイプライン（Phase 2）

### ツール・ライブラリ（tools/）
- email_extractor.py - メールアドレス抽出
- email_generator.py - Gemini でメール生成
- email_sender.py - SMTP でメール送信
- crm_manager.py - Google Sheets CRM 操作
- db_manager.py - SQLite 送信ログ管理
- その他 103 ファイル

### データベース
- logs/send_log.db - メール送信・バウンスログ
- html_cache.db - Web スクレイピングキャッシュ

### Google Sheets CRM
- シート: SNS動画活用企業向け営業CRM管理シート
- 対象: YouTube チャンネル lead (1705 件)
- メール対象: 341 件（A/B ランク、NG フラグ FALSE）

## 実行方法

### 日次運用（推奨）
スケジュールタスク DailyEmailOperations が毎日 09:00 に自動実行。

### 手動実行
python daily_operations.py --limit 15

### ドライラン（テスト）
python send_email.py --limit 15 --dry-run

## 本日の修正（2026-04-21）

### send_email.py のロジック改善

問題点: 70/30 配分のはずが、実際には 10 件で停止していた。

原因: 
- リピート候補が「3 日経過していない」ため送信できず
- リピート不足分を補填するロジックがなかった

修正内容:
1. 初回とリピートを明確に分離
2. リピート不足分を初回で補填する設計
3. 初回 15 件全て送信の仕様に統一
4. dry-run で動作確認完了

結果: 
- 15 件の初回メール生成（エラーなし）
- 補填ロジック正常動作
- 本番環境への展開準備完了

## 設定値

| 項目 | 値 | 備考 |
|------|-----|------|
| daily_limit | 15 件 | 毎日の送信上限 |
| EMAIL_FIRST_SEND_RATIO | 70% | 初回配分比率 |
| EMAIL_FOLLOWUP_SEND_RATIO | 30% | リピート配分比率 |
| EMAIL_INTERVAL_DAYS | 3 | リピート待機日数 |
| EMAIL_MAX_SEQUENCE | 4 | 最大送信回数 |
| WARMUP_SCHEDULE | 1:10, 2:15, 3:20, 4:25 | ウォーミング送信スケジュール |

## 今後のロードマップ

### Phase 1（現在）
- lead 収集パイプライン構築 ✅
- メール送信エンジン構築 ✅
- 初回/リピート分離ロジック実装 ✅
- 本番運用テスト（2026-04-22 以降）

### Phase 2（予定）
- Step 6b フォーム自動送信の実装
- collect.py の Email 抽出率向上（現在 20% → 目標 50%）
- リプライ率計測・分析

### Phase 3+（将来）
- Website Scraper v2（URL 抽出パイプライン拡張）
- AI による返信内容解析
- 営業ファネル可視化

## トラブルシューティング

### メール送信が 15 件未満で止まる場合
1. CRM の「メール送信対象」件数を確認（get_pending_leads() で 341 件以上が必要）
2. send_log.db の送信履歴を確認（同日 4 通以上は送信不可）
3. バウンス率を確認（高い場合は対象から除外）

### Google Sheets 接続エラー
1. credentials.json の存在確認
2. SPREADSHEET_ID の設定確認
3. Google API のクォータ確認

## ドキュメント一覧

- README.md（本ファイル）
- CHECKLIST.md - 実装チェックリスト
- PROJECT_STATUS.md - 詳細進捗状況
- email_extractor_SPECIFICATION.md - メール抽出仕様書
- STEP6B_IMPLEMENTATION_SUSPENSION.md - Step 6b 延期理由
- PHONE_EXTRACTION_DESIGN.md - 電話番号抽出パイプライン設計

### website_scraper_v2.py - Web スクレイピング & 電話番号抽出
- 目的: CRM の公式サイト URL から企業情報（電話番号等）を抽出
- 機能:
  - HTML クロール（複数ページを自動検索）
  - 企業名抽出（OG タグ、JSON-LD、title タグから優先度順に抽出）
  - 電話番号抽出（tel リンク、JSON-LD、メタタグ、正規表現から多段階抽出）
  - キャッシング機能（HTML キャッシュで API 効率化）
- 出力先: Google Sheets Phase 5 ファイル（SPREADSHEET_ID_PHASE5）
- 状態: 実装済み（2026-04-18）、現在修正中（出力先の正規化）
- 詳細: PHONE_EXTRACTION_DESIGN.md 参照

