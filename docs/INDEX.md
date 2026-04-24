# Documentation Index

## ドキュメント一覧（2026-04-24 更新）

### プロジェクト概要
- README.md
  プロジェクト概要・使用方法・セットアップ
  
- docs/INDEX.md
  ドキュメント一覧・クイックリファレンス（本ファイル）

### 現在のステータス
- CURRENT_STATUS.md
  **プロジェクト全体の最新進捗（Phase 1-7）**
  最終更新: 2026-04-24

### システム設計
- docs/ARCHITECTURE.md
  システム全体構成・データフロー・DB スキーマ

- docs/IMPLEMENTATION.md
  各モジュールの実装詳細・関数説明

### フェーズ別ガイド

**Phase 5: ウェブサイトスクレイピング** ✅ 完了
- docs/PHASE5_GUIDE.md
  Phase 5 の実装ガイド・抽出フロー
  
**Phase 6: ZeroBounce メール検証** ✅ 完成（2026-04-24）
- PHASE6_GUIDE.md
  **Phase 6 実行ガイド（ZeroBounce API 統合）**
  最終更新: 2026-04-24

**Phase 7: メール送信改善** ✅ 完成（2026-04-24）
- send_email.py 改善：Phase 6 検証結果チェック追加
- crm_manager.py 改善：get_pending_leads() に検証フィルタ

### 運用ガイド
- OPERATION_GUIDE.md
  **日次/週次/月次運用マニュアル（本番運用用）**
  最終更新: 2026-04-24

### 抽出・検証仕様
- docs/EXTRACTION_GUIDE.md
  電話番号とメール抽出の仕様・パターン

- docs/API_REFERENCE.md
  phone_extractor・email_extractor の API

### 設定・トラブル
- docs/CONFIGURATION.md
  config.py の全設定項目の説明

- docs/EXAMPLES.md
  実行例・期待出力・ログサンプル

- docs/FAQ.md
  よくある質問と回答

- docs/TROUBLESHOOTING.md
  エラー原因と解決方法

---

## ドキュメント読む順序

### 新規参加者向け
1. README.md を読む
2. CURRENT_STATUS.md で最新進捗を確認
3. docs/ARCHITECTURE.md で構成を理解
4. docs/EXAMPLES.md で実行例を確認

### 本番運用者向け
1. OPERATION_GUIDE.md で日次運用方法を確認
2. PHASE6_GUIDE.md で検証方法を確認
3. docs/TROUBLESHOOTING.md でエラー対応を確認

### 開発者向け
1. CURRENT_STATUS.md で完成機能を確認
2. docs/IMPLEMENTATION.md で関数詳細を確認
3. docs/API_REFERENCE.md で API を確認
4. docs/CONFIGURATION.md で設定を確認

### トラブル発生時
1. docs/TROUBLESHOOTING.md でエラーを検索
2. docs/FAQ.md で一般的な質問を検索
3. logs/send_email.log または logs/website_scraper.log でログ確認

---

## クイックコマンド

### Phase 5: ウェブサイトスクレイピング
python website_scraper.py --clear-cache  # 本格実行
python website_scraper.py --limit=10     # テスト実行（10件）

### Phase 6: メール検証（ZeroBounce）
python bounce_checker.py 100              # テスト（最初の100件）
python bounce_checker.py 1589             # 本格実行（全件）

### Phase 7: メール送信
python send_email.py --limit 20 --dry-run  # テスト
python send_email.py --limit 20            # 本番

### 日次運用
python daily_operations.py                # 一括実行（バウンス検出 → 送信 → ログ記録）
python daily_metrics_logger.py            # 日次メトリクス記録

### ログ確認
Get-Content logs/send_email.log -Tail 50
Get-Content logs/website_scraper.log -Tail 50
Get-Content logs/bounce_checker.log -Tail 50

### DB 初期化
rm logs/phase5_data.db
rm logs/html_cache.db
rm logs/send_email.db

---

## 実行フロー

### Phase 5 → Phase 6 → Phase 7 → 本番運用

1. **Phase 5 完了**（ウェブサイトスクレイピング）
   python website_scraper.py --clear-cache

2. **Phase 6 実行**（ZeroBounce メール検証）
   python bounce_checker.py 1589

3. **送信対象リスト作成**
   python create_sendable_list.py

4. **メール送信開始**（Phase 7）
   python send_email.py --limit 20

5. **日次運用開始**
   python daily_operations.py  # 毎日 9:00 に自動実行

---

## ファイル構成

video-sales-automation-phase1/
├── website_scraper.py          (Phase 5)
├── bounce_checker.py           (Phase 6)
├── send_email.py               (Phase 7)
├── daily_operations.py         (日次スケジューラ)
├── daily_metrics_logger.py     (日次ログ記録)
├── create_sendable_list.py     (送信対象リスト作成)
├── crm_manager.py
├── db_manager.py
├── db_manager_phase5.py
├── email_generator.py
├── email_sender.py
├── config.py
├── .env                        (環境変数・API キー)
├── tools/
│   ├── phone_extractor.py
│   ├── email_extractor.py      (修正: 画像ファイル・テスト除外)
│   ├── website_crawler.py
│   ├── company_info_extractor.py
│   └── cache_manager.py
├── logs/
│   ├── website_scraper.log
│   ├── send_email.log
│   ├── bounce_checker.log
│   ├── daily_metrics.jsonl     (日次ログ JSON)
│   ├── phase5_data.db          (SQLite: クロール結果 + 検証結果)
│   ├── html_cache.db           (SQLite: HTML キャッシュ)
│   └── send_email.db           (SQLite: 送信履歴)
├── docs/
│   ├── INDEX.md                (本ファイル)
│   ├── ARCHITECTURE.md
│   ├── IMPLEMENTATION.md
│   ├── PHASE5_GUIDE.md
│   ├── EXTRACTION_GUIDE.md
│   ├── CONFIGURATION.md
│   ├── API_REFERENCE.md
│   ├── EXAMPLES.md
│   ├── FAQ.md
│   └── TROUBLESHOOTING.md
├── CURRENT_STATUS.md           (最新ステータス)
├── PHASE6_GUIDE.md             (Phase 6 ガイド)
├── OPERATION_GUIDE.md          (日次運用マニュアル)
└── README.md

---

## Phase 進捗

| Phase | 名称 | ステータス | 最終更新 |
|-------|------|----------|---------|
| 1 | YouTube チャンネル収集 | ✅ 完了 | 2026-04-17 |
| 2 | 営業メール送信 | ✅ 完了 | 2026-04-19 |
| 3 | バウンス管理 | ✅ 完了 | 2026-04-17 |
| 4 | メール抽出・有効性チェック | ✅ 完了 | 2026-04-20 |
| 5 | ウェブサイトスクレイピング | ⏳ 進行中（71%） | 2026-04-24 |
| 6 | ZeroBounce メール検証 | ✅ 完成 | 2026-04-24 |
| 7 | メール送信改善 | ✅ 完成 | 2026-04-24 |
| 8 | Google Sheets API 統合 | ⏳ 計画中 | 2026-04-24 |

---

## KPI 一覧

### 月次 KPI
- 実送信件数: 500-800 件
- 総バウンス率: 10-20%
- 開封率: 15-25%
- クリック率: 2-5%
- 返信率: 1-3%
- 商談化率: 0.2-1%

### 日次ログ（行動指標）
- Raw 取得数
- 有効数
- 実送信数
- メモ

---

**最終更新**: 2026-04-24 17:30
**作成者**: AI Assistant
**ステータス**: 本番運用準備完了
