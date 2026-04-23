# FAQ (Frequently Asked Questions)

## 実行に関する質問

Q: 実行にどのくらい時間がかかりますか？
A: 1 URL あたり 10-30 秒（20 ページクロール + 抽出）
   全 1,589 URL → 推定 4-8 時間（シングルスレッド）
   ネットワーク速度により変動します

Q: --limit オプションの使い方は？
A: python website_scraper.py --limit=3
   最初の3件だけ処理（テスト用）
   limit なし: python website_scraper.py (全件処理)

Q: 途中で中断したら、続きから実行できますか？
A: はい。DB に保存済みの URL は自動でスキップされます
   continue 機能は実装済み

Q: 複数回実行しても大丈夫ですか？
A: はい。同じ URL は check_url_exists() で除外されます
   重複データの心配はありません

## 抽出に関する質問

Q: 電話番号が見つかりません
A: 以下を確認してください:
   1. config.PHONE_PATTERNS を確認
   2. 対象サイトに電話番号が掲載されているか
   3. ページ数を増やす (MAX_CRAWL_PAGES)
   4. is_valid_phone() の検証ロジックが厳しくないか

Q: メールアドレスが見つかりません
A: 以下を確認してください:
   1. 対象サイトに公開メールアドレスがあるか
   2. email_extractor.py のドメイン検証が除外していないか
   3. regex パターンが対応しているか
   4. お問い合わせページなどに掲載されているか

Q: 複数の電話番号が見つかった場合は？
A: 最初の1件を保存します
   複数保存は未実装

Q: 複数のメールアドレスが見つかった場合は？
A: 最初の1件を保存します
   複数保存は未実装

Q: "None" と空文字列の違いは？
A: 抽出を試みたが見つからなかった = "None" 文字列
   未実装の箇所 = 空文字列 ("")
   デバッグ時に区別するため

## Google Sheets に関する質問

Q: Phase 5 シートの列を変更したい
A: config.py と crm_manager.py の append_to_gsheet_phase5()
   を修正してください
   現在: A=company, B=url, C=phone, D=email, E=source,
         F=status, G=scraped_at

Q: CRM シートとのデータ同期は？
A: CRM シートから読み込むのは最初だけです
   変更があれば再実行してください（重複は自動除外）

Q: Phase 5 シートを手動で編集しても大丈夫？
A: status や memo などの追加列は OK
   スクレイピング結果の列（A-G）は編集しないでください

Q: シートのヘッダー行は消しても大丈夫？
A: いいえ。ヘッダー行は必須です
   削除したら append_row() でエラーになります

## データに関する質問

Q: 保存されたデータのバックアップは？
A: Google Sheets は自動保存されます
   DB は logs/phase5_data.db を手動バックアップ推奨

Q: 古いデータを削除したい
A: 1. Google Sheets から手動削除（ヘッダー保持）
   2. DB をリセット: rm logs/phase5_data.db
   3. キャッシュをクリア: rm logs/html_cache.db

Q: status = "invalid" のデータを再処理できますか？
A: DB から該当行を削除してから再実行してください

## トラブルに関する質問

Q: "credentials.json not found" エラー
A: Google Sheets API の認証ファイルが必要です
   取得方法: Google Cloud Console → OAuth 2.0 認証情報
   保存場所: プロジェクトルート

Q: "Access Denied" エラー
A: SPREADSHEET_ID_PHASE5 が間違っているか
   アクセス権限がない可能性があります
   シェア設定を確認してください

Q: "database is locked" エラー
A: 複数プロセスが同時アクセスしています
   既に実行中のプロセスを停止してください

Q: メモリ不足
A: --limit オプションで分割実行してください
   例: python website_scraper.py --limit=100



## Phase 5 関連 Q&A

### Q: Phase 5 の実行時間はどのくらい？

A: 1,589 URL で約 7 時間（シングルスレッド）。1 URL あたり平均 15.9 秒。ネットワーク遅延により変動します。

### Q: 電話番号が検出されない場合は？

A: 以下を確認してください：
- config.PHONE_PATTERNS を確認
- tools/phone_extractor.py の is_valid_phone() ロジックを確認
- サンプル HTML で動作テスト
- MAX_CRAWL_PAGES を増やす（デフォルト 20 ページ）
- ウェブサイトに公開電話番号がない可能性

### Q: メールアドレスが検出されない場合は？

A: 以下を確認してください：
- サイトに公開メールアドレスがあるか確認
- tools/email_extractor.py の invalid_domains リストを確認
- ドメイン検証を一時的に無効化してテスト
- regex パターンを拡張

### Q: 電話番号が複数ある場合、どれが保存される？

A: 最初に見つかった 1 つのみ保存されます。複数抽出は未実装。

### Q: Phase 5 を再実行する場合は？

A: DB に存在する URL は自動的にスキップされます。すべてを再処理したい場合：
- rm logs/phase5_data.db で DB を削除
- python website_scraper.py で再実行

### Q: Google Sheet Phase 5 のカラムを変更したい場合は？

A: config.py と crm_manager.py の append_to_gsheet_phase5() を編集してください。現在の順序：
A=company_name, B=website_url, C=phone, D=email, E=source_page, F=status, G=scraped_at

### Q: Phase 5 データをバックアップしたい場合は？

A: 以下をバックアップしてください：
- logs/phase5_data.db（メインデータ）
- Google Sheet Phase 5（自動保存）
- logs/website_scraper.log（処理履歴）

### Q: 古いデータを削除したい場合は？

A: 以下の手順で削除：
1. Google Sheet Phase 5 から該当行を削除（ヘッダは保持）
2. rm logs/phase5_data.db で DB をリセット
3. rm logs/html_cache.db でキャッシュをリセット
4. python website_scraper.py で再実行

### Q: status が "invalid" の理由は？

A: 電話番号が見つからなかった場合。メール検出状況は status に影響しません。

### Q: 特定の URL だけ再処理したい場合は？

A: その URL を DB から削除してから再実行：
python -c "import sqlite3; conn = sqlite3.connect('logs/phase5_data.db'); conn.execute('DELETE FROM phase5_data WHERE url=\"https://example.com\"'); conn.commit(); conn.close()"

