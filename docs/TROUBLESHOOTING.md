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

