# Troubleshooting Guide

## Google Sheets 認証エラー

エラー: "credentials.json not found"
原因: Google Sheets API 認証ファイルが無い
解決:
  - Google Cloud Console で OAuth 2.0 認証情報を作成
  - credentials.json をプロジェクトルートに配置
  - crm_manager.py の get_crm() が読み込むことを確認

エラー: "Access Denied"
原因: SPREADSHEET_ID_PHASE5 が間違っている or アクセス権限なし
解決:
  - config.py で SPREADSHEET_ID_PHASE5 を確認
  - Google Sheets のシェア設定を確認
  - サービスアカウントのメールアドレスにアクセス権を付与

## HTML クロール失敗

エラー: "HTML 取得失敗"
原因: ネットワーク問題 or robots.txt 制限
解決:
  - crawl_domain() のタイムアウト値を増やす (config.TIMEOUT)
  - robots.txt を確認
  - ネットワーク接続を確認

エラー: メモリ不足
原因: 大量の HTML を保持しすぎ
解決:
  - --limit オプションで分割実行
  - キャッシュを削除: rm logs/html_cache.db
  - MAX_CRAWL_PAGES を減らす (config.py)

## 抽出結果が空

電話番号が全く見つからない
原因: 正規表現パターンが不十分
解決:
  - config.PHONE_PATTERNS を確認・拡張
  - phone_extractor.py の is_valid_phone() ロジック確認
  - サンプル HTML で手動テスト

メールアドレスが全く見つからない
原因: ドメイン検証が厳しすぎる or パターン不足
解決:
  - email_extractor.py の invalid_domains を確認
  - ドメイン検証を一時的に無効化してテスト
  - regex パターンを拡張

## データベース問題

エラー: "database is locked"
原因: 複数プロセスが同時アクセス
解決:
  - 既に実行中のプロセスを停止
  - DB ファイルをロック解除: rm logs/phase5_data.db

エラー: "duplicate entry"
原因: 同じ URL が複数回追記された
解決:
  - check_url_exists() が正常に動作しているか確認
  - DB を初期化: rm logs/phase5_data.db

## ログ・デバッグ

ログファイル: logs/website_scraper.log
最後の100行を確認:
  Get-Content logs/website_scraper.log -Tail 100

全ログを検索:
  Select-String -Path logs/website_scraper.log -Pattern "エラー"

デバッグモード有効化:
  - website_scraper.py の logger.setLevel() を DEBUG に変更
  - 詳細ログを出力

## リセット手順

すべてのデータを初期化:
  rm logs/phase5_data.db
  rm logs/html_cache.db
  Google Sheets Phase 5 を開き、ヘッダー行以外を削除

部分的なリセット:
  - DB のみ: rm logs/phase5_data.db
  - キャッシュのみ: rm logs/html_cache.db
  - Sheet のみ: 手動で削除



## Phase 5 トラブルシューティング

### 電話番号が検出されない

症状: status が "invalid" ばかり

対応:
1. サイトに公開電話番号があるか確認
2. config.PHONE_PATTERNS を確認、必要に応じて拡張
3. MAX_CRAWL_PAGES を 20 から 50 に増やす
4. tools/phone_extractor.py の is_valid_phone() ロジックをログ出力で確認
5. サンプル URL で手動テスト：
   python -c "
   from tools.phone_extractor import extract_phone
   from tools.website_crawler import crawl_domain
   html = crawl_domain('https://example.com')
   phone = extract_phone(html)
   print(f'Phone: {phone}')
   "

### メールアドレスが検出されない

症状: email カラムが "None" ばかり

対応:
1. ウェブサイトに公開メールアドレスがあるか確認
2. tools/email_extractor.py の invalid_domains リストが過度に制限していないか確認
3. email regex パターン（config.EMAIL_PATTERN）を確認
4. 一時的に is_valid_email() のドメイン検証を無効化してテスト
5. サンプル URL で手動テスト：
   python -c "
   from tools.email_extractor import extract_email
   from tools.website_crawler import crawl_domain
   html = crawl_domain('https://example.com')
   email = extract_email(html)
   print(f'Email: {email}')
   "

### HTML クロール失敗（Timeout）

症状: "Timeout" エラーが出続ける

対応:
1. config.TIMEOUT を 10 秒から 30 秒に増やす
2. ネットワーク接続を確認
3. ウェブサイトが robots.txt で制限していないか確認
4. USER_AGENT をブラウザ風に変更（config.py）
5. MAX_CRAWL_PAGES を 20 から 10 に減らす
6. 該当 URL をスキップしたい場合、DB から削除：
   python -c "import sqlite3; conn = sqlite3.connect('logs/phase5_data.db'); conn.execute('DELETE FROM phase5_data WHERE url=\"https://example.com\"'); conn.commit(); conn.close()"

### メモリ不足エラー

症状: "MemoryError" または "Process terminated"

対応:
1. --limit オプションで分割実行：
   python website_scraper.py --limit=100
2. HTML キャッシュを削除：
   rm logs/html_cache.db
3. config.MAX_CRAWL_PAGES を 20 から 10 に減らす
4. 不要な logs を削除：
   rm logs/website_scraper.log

### データベースがロックされている

症状: "database is locked" エラー

対応:
1. 他のプロセスで DB を開いていないか確認
2. DB ファイルを削除して再初期化：
   rm logs/phase5_data.db
   python website_scraper.py --limit=1
3. PowerShell を再起動

### Google Sheets API エラー

症状: "Access Denied" または "Not Found"

対応:
1. credentials.json が project root に存在するか確認
2. SPREADSHEET_ID_PHASE5 が正しいか config.py で確認
3. Google Sheet の共有設定を確認（service account にアクセス権があるか）
4. Google Cloud Console で API が有効になっているか確認
5. credentials.json を再生成してみる

### "credentials.json not found" エラー

症状: Google Sheets 認証失敗

対応:
1. Google Cloud Console で OAuth 2.0 credentials を作成
2. credentials.json をダウンロード
3. project root に配置
4. crm_manager.py が credentials.json を正しく読み込んでいるか確認

### 重複 URL のスキップが機能しない

症状: 同じ URL が複数回処理されている

対応:
1. DB に UNIQUE 制約があるか確認：
   python -c "import sqlite3; conn = sqlite3.connect('logs/phase5_data.db'); cursor = conn.cursor(); cursor.execute(\"PRAGMA index_info(phase5_data)\"); print(cursor.fetchall()); conn.close()"
2. DB を再初期化：
   rm logs/phase5_data.db
   python website_scraper.py --limit=1

### ログファイルが見つからない

症状: logs/website_scraper.log が存在しない

対応:
1. logs/ フォルダが存在するか確認
2. フォルダがない場合、作成：
   mkdir logs
3. python website_scraper.py で再実行

### 進捗が進まない（無限ループ）

症状: Progress が更新されない

対応:
1. Ctrl+C で中断
2. ログを確認：
   Get-Content logs/website_scraper.log -Tail 100
3. 問題の URL をスキップして再開：
   python -c "import sqlite3; conn = sqlite3.connect('logs/phase5_data.db'); conn.execute('DELETE FROM phase5_data WHERE url=\"https://problematic-url.com\"'); conn.commit(); conn.close()"
4. キャッシュをクリア：
   rm logs/html_cache.db

### Phase 5 完全リセット

すべてをやり直したい場合:
rm logs/phase5_data.db
rm logs/html_cache.db
Google Sheet Phase 5 から全行削除（ヘッダは保持）
python website_scraper.py で再実行

