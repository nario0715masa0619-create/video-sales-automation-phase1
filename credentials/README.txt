認証ファイルの配置場所

このフォルダに以下のファイルを配置してください:

1. service_account.json
   Google Cloud Console > IAMと管理 > サービスアカウント
   → キーを作成 > JSON でダウンロード

2. oauth_credentials.json
   Google Cloud Console > 認証情報 > OAuth 2.0クライアントID
   → デスクトップアプリ で作成 > JSON でダウンロード

3. gmail_token.json
   python email_sender.py を実行すると自動生成されます
