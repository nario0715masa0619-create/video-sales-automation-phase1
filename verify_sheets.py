"""
Google Sheets API 接続確認スクリプト
実行方法: python verify_sheets.py
"""
import os
import json
import sys

def check_credentials():
    """認証ファイルの存在と内容を確認"""
    cred_paths = [
        "credentials/service_account.json",
        os.path.join(os.environ.get('APPDATA', ''), 'gspread', 'service_account.json'),
    ]
    
    found_path = None
    for path in cred_paths:
        if os.path.exists(path):
            found_path = path
            break
    
    if not found_path:
        print("❌ 認証ファイルが見つかりません")
        print("   以下のいずれかに配置してください:")
        for p in cred_paths:
            print(f"   - {p}")
        return None
    
    print(f"✅ 認証ファイル発見: {found_path}")
    
    try:
        with open(found_path, 'r') as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        for field in required_fields:
            if field in creds:
                if field == 'client_email':
                    print(f"✅ {field}: {creds[field]}")
                elif field == 'private_key':
                    print(f"✅ {field}: [設定済み]")
                else:
                    print(f"✅ {field}: {creds[field]}")
            else:
                print(f"❌ {field}: 欠落")
                return None
        
        if creds.get('type') != 'service_account':
            print(f"❌ typeが service_account ではありません: {creds.get('type')}")
            return None
            
        return creds
    except json.JSONDecodeError as e:
        print(f"❌ JSONパースエラー: {e}")
        return None

def test_sheets_connection(creds):
    """Google Sheets への接続テスト"""
    try:
        import gspread
        print("\n📊 gspread インポート成功")
    except ImportError:
        print("❌ gspread がインストールされていません")
        print("   実行: pip install gspread")
        return False
    
    try:
        gc = gspread.service_account(filename="credentials/service_account.json")
        print("✅ Google Sheets API 認証成功！")
        
        # スプレッドシート一覧を取得してみる（共有されているもの）
        spreadsheets = gc.list_spreadsheet_files()
        print(f"✅ アクセス可能なスプレッドシート数: {len(spreadsheets)}")
        if spreadsheets:
            for ss in spreadsheets[:3]:
                print(f"   - {ss['name']}")
        else:
            print("   （まだ共有されたスプレッドシートはありません）")
        
        return True
    except Exception as e:
        print(f"❌ 接続エラー: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Google Sheets API 接続確認")
    print("=" * 50)
    
    print("\n【STEP 1】認証ファイル確認")
    creds = check_credentials()
    
    if creds:
        print("\n【STEP 2】接続テスト")
        success = test_sheets_connection(creds)
        
        if success:
            print("\n🎉 設定完了！orchestrator.py を実行できます")
        else:
            print("\n⚠️  接続に失敗しました。上記エラーを確認してください")
    else:
        print("\n⚠️  認証ファイルを配置してから再実行してください")
        print("\n【認証ファイル取得手順】")
        print("1. https://console.cloud.google.com/ にアクセス")
        print("2. プロジェクト作成 → Google Sheets API & Drive API を有効化")
        print("3. IAM & Admin → Service Accounts → サービスアカウント作成")
        print("4. Keys タブ → ADD KEY → JSON → ダウンロード")
        print("5. ダウンロードしたファイルを credentials/service_account.json に配置")
