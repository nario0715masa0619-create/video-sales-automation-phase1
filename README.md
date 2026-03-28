# 動画スクレイピング × 自動営業フロー Phase 1

> YouTubeチャンネルをスクレイピングして企業リードを自動抽出し、Gemini AI でパーソナライズされた営業メールを Gmail から自動送信するシステムです。

---

## 🗂️ ファイル構成

```
.
├── config.py                  # 設定値の一元管理
├── target_scraper.py          # YouTubeチャンネルスクレイピング
├── scorer.py                  # スコアリング（100点満点）
├── crm_manager.py             # Google Sheets CRM 操作
├── email_generator.py         # Gemini API メール文生成
├── email_sender.py            # Gmail API メール送信
├── orchestrator.py            # 統合メイン処理 & Flask API
├── requirements.txt           # 必要ライブラリ
├── .env.example               # 環境変数テンプレート
├── credentials/               # 認証ファイル格納フォルダ（要作成）
│   ├── service_account.json   # Google サービスアカウントキー
│   ├── oauth_credentials.json # Gmail OAuth2 認証ファイル
│   └── gmail_token.json       # Gmail トークン（初回認証後に自動生成）
├── logs/                      # ログファイル（自動生成）
└── deploy/
    └── cloud_function_setup.sh # GCP デプロイスクリプト
```

---

## 🚀 セットアップ手順

### Step 1: Python 環境の準備

```bash
# Python 3.11 以上を推奨
python --version  # 3.11 or 3.12

# 仮想環境の作成（推奨）
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate   # Windows

# ライブラリのインストール
pip install -r requirements.txt
```

---

### Step 2: 環境変数の設定

```bash
# .env.example をコピー
cp .env.example .env

# .env をエディタで開いて各値を設定
nano .env   # または code .env など
```

**最低限設定が必要な項目：**

| 変数名 | 説明 | 取得場所 |
|--------|------|---------|
| `SPREADSHEET_ID` | Google スプレッドシートの ID | シートのURL（`/d/` と `/edit` の間） |
| `GEMINI_API_KEY` | Gemini API キー | [Google AI Studio](https://aistudio.google.com/) |
| `GMAIL_SENDER_ADDRESS` | 送信元 Gmail アドレス | Googleアカウント設定 |
| `SERPAPI_KEY` | SerpAPI キー（チャンネル検索用） | [serpapi.com](https://serpapi.com/) |
| `MY_COMPANY_NAME` | 自社名（メール署名） | 任意 |
| `MY_NAME` | 担当者名（メール署名） | 任意 |

---

### Step 3: Google API 認証設定

#### 3-1. サービスアカウントの設定（Google Sheets 用）

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新規プロジェクトを作成（または既存を選択）
3. 「API とサービス」→「ライブラリ」で以下を有効化：
   - **Google Sheets API**
   - **Google Drive API**
4. 「IAM と管理」→「サービスアカウント」→「サービスアカウントを作成」
5. 作成後、「キー」タブ →「鍵を追加」→「JSON」でダウンロード
6. ダウンロードしたファイルを `credentials/service_account.json` に配置
7. **スプレッドシートを サービスアカウントのメールアドレスと共有する**（編集権限）

```bash
# credentials フォルダを作成
mkdir -p credentials

# サービスアカウントのメールアドレスを確認
cat credentials/service_account.json | python -c "import json,sys; d=json.load(sys.stdin); print(d['client_email'])"
# → xxxx@your-project.iam.gserviceaccount.com
# このアドレスでスプレッドシートを共有してください
```

#### 3-2. Gmail OAuth2 認証設定（Gmail 送信用）

1. Google Cloud Console → 「API とサービス」→「ライブラリ」で **Gmail API** を有効化
2. 「OAuth 同意画面」を設定（外部・テストユーザーを追加）
3. 「認証情報」→「認証情報を作成」→「OAuth 2.0 クライアント ID」
   - アプリケーションの種類: **デスクトップアプリ**
4. JSON をダウンロードし、`credentials/oauth_credentials.json` に配置
5. 初回実行時にブラウザが開くので、送信元 Gmail アカウントで認証する

```bash
# 初回認証（ブラウザが開きます）
python email_sender.py

# 認証後、credentials/gmail_token.json が自動生成されます
# 2回目以降はブラウザが開きません
```

---

### Step 4: Gemini API キーの設定

1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. 「APIキーを作成」をクリック
3. 生成されたキーを `.env` の `GEMINI_API_KEY` に設定

---

### Step 5: SerpAPI キーの設定（チャンネル検索用）

1. [serpapi.com](https://serpapi.com/) に登録
2. ダッシュボードから API キーをコピー
3. `.env` の `SERPAPI_KEY` に設定

> **無料プランについて:** 無料枠は月100回まで。1回の実行でキーワード数分消費します（デフォルト5回）。月20回の実行なら無料枠内に収まります。

---

### Step 6: 設定確認

```bash
# 設定値の確認
python config.py

# 出力例:
# ✅ 全設定値が正常にロードされました
#    SPREADSHEET_ID: 1BxiMVs0X...
#    GEMINI_MODEL: gemini-1.5-flash
#    EMAIL_MAX_SEQUENCE: 4通
#    EMAIL_TARGET_RANKS: ['A', 'B']
```

---

## 🏃 実行方法

### ローカルでの実行

```bash
# ドライラン（メール送信なし）で動作確認
python orchestrator.py --mode dry-run

# フル実行（スクレイピング + スコアリング + メール送信）
python orchestrator.py --mode run

# メール送信のみ（スクレイピングスキップ）
python orchestrator.py --mode email-only

# 検索キーワードを指定してフル実行
python orchestrator.py --mode run --keywords "YouTube 企業 商品紹介" "YouTube D2C ブランド"

# Flask API サーバーとして起動
python orchestrator.py --mode api
```

### 各モジュールの単体テスト

```bash
# スコアリングのテスト
python scorer.py

# チャンネルスクレイピングのテスト（URL指定）
python target_scraper.py https://www.youtube.com/@企業チャンネル名

# メール生成のテスト
python email_generator.py

# Gmail 接続確認
python email_sender.py

# Gmail テスト送信（自分自身に送信）
python email_sender.py --send-test
```

---

## ☁️ Google Cloud Functions へのデプロイ（週次自動実行）

```bash
# デプロイスクリプトを実行
chmod +x deploy/cloud_function_setup.sh

# GCP_PROJECT_ID を設定してからデプロイ
nano deploy/cloud_function_setup.sh  # GCP_PROJECT_ID を変更

./deploy/cloud_function_setup.sh
```

デプロイ後は **毎週月曜日 AM9:00 JST** に自動実行されます。

### ログの確認

```bash
# リアルタイムログ
gcloud functions logs read video-sales-weekly-flow \
    --region=asia-northeast1 \
    --limit=50
```

---

## 🔄 n8n / Make からの実行

Flask API を起動して外部からトリガーできます。

### API エンドポイント一覧

| エンドポイント | メソッド | 説明 |
|-------------|---------|------|
| `GET /api/health` | GET | ヘルスチェック |
| `POST /api/run` | POST | フル実行（スクレイピング+メール送信） |
| `POST /api/run-email-only` | POST | メール送信のみ |

### n8n からの呼び出し例

```json
// POST /api/run
// Headers: Authorization: Bearer <API_SECRET_TOKEN>
{
  "skip_scraping": false,
  "dry_run": false,
  "keywords": ["YouTube 企業 ビジネス"]
}
```

### レスポンス例

```json
{
  "success": true,
  "duration_seconds": 240,
  "stats": {
    "channels_found": 30,
    "channels_passed_icp": 12,
    "leads_upserted": 12,
    "leads_pending": 8,
    "emails_generated": 8,
    "emails_sent": 8,
    "emails_bounced": 0
  },
  "errors": []
}
```

---

## 📊 スコアリング設計

総合スコア = 100点満点（4指標の合計）

| 指標 | 最大点数 | 計算方法 |
|------|---------|---------|
| 投稿頻度 | 30点 | 直近3ヶ月: 12本以上→30点、8本→20点、4本→10点 |
| 平均再生数 | 25点 | 登録者比: 10%以上→25点、5%→15点、2%→8点 |
| エンゲージメント率 | 25点 | 5%以上→25点、3%→15点、1%→8点 |
| 成長トレンド | 20点 | 直近1ヶ月 vs 3ヶ月平均: 120%以上→20点、100%→12点、80%→6点 |

**ランク基準:** A=70点以上 / B=40〜69点 / C=39点以下

---

## 📝 CRM（スプレッドシート）設計

**Leads シート（メインCRM）** - 36列構成

主要列: 会社名 / メールアドレス / チャンネルURL / スコア指標 / ランク / 営業ステータス / 送信回数 / 送信日 / 各種フラグ

**メール送信ログシート** - 11列構成

**マスタ設定シート** - スコアリング設定・NGリスト

---

## ⚙️ 設定のカスタマイズ

`config.py` を編集するか、`.env` ファイルで以下を変更できます：

```python
# ICP条件の変更
ICP_MIN_SUBSCRIBERS = 500    # 最小登録者数
ICP_MAX_SUBSCRIBERS = 50000  # 最大登録者数
ICP_MIN_VIDEOS_3M   = 4      # 直近3ヶ月の最低投稿本数

# メールシーケンスの変更
EMAIL_MAX_SEQUENCE     = 4   # 最大送信通数（3〜5に変更可）
EMAIL_INTERVAL_DAYS    = 4   # 送信間隔（営業日数）
EMAIL_MAX_SEND_PER_RUN = 20  # 1回の実行での最大送信数
```

---

## 🔧 トラブルシューティング

### よくあるエラーと解決方法

| エラー | 原因 | 解決方法 |
|--------|------|---------|
| `SPREADSHEET_ID が未設定` | .env の設定漏れ | SPREADSHEET_ID を設定する |
| `Service account file not found` | 認証ファイルがない | credentials/ フォルダにJSONを配置 |
| `Permission denied for Sheets` | スプレッドシートが共有されていない | サービスアカウントのメールでシートを共有 |
| `Gmail authentication required` | OAuth2 認証がまだ | `python email_sender.py` で初回認証を完了 |
| `SerpAPI 0件` | APIキーが未設定または無効 | SERPAPI_KEY を確認する |
| `Gemini API error` | APIキーが未設定 | GEMINI_API_KEY を確認する |
| `yt-dlp エラー` | yt-dlp のバージョン切れ | `pip install -U yt-dlp` で更新 |

---

## 📅 月次レビューガイド（月5時間以内の運用）

毎月1回、以下をチェックするだけで OK です：

- [ ] Google Sheets でAランクリード数と返信率を確認（約10分）
- [ ] 返信があった企業のステータスを更新（約10分）
- [ ] 開封率が低い場合は件名テンプレートを修正（約15分）
- [ ] スコアリング閾値の微調整（必要な場合のみ）（約30分）

---

## 🔮 将来の拡張計画

| Phase | 内容 |
|-------|------|
| Phase 2 | YouTube Data API v3 に移行（スクレイピング精度向上） |
| Phase 3 | TikTok / Instagram Reels への対応 |
| Phase 4 | SendGrid への移行（大量送信対応） |
| Phase 5 | 開封・クリックトラッキング（ピクセル埋め込み） |
| Phase 6 | 外部展開用にモジュールをパッケージ化 |

---

## 📄 ライセンス

このシステムは自社運用を目的として開発されています。
外部展開・再配布の際は適切なライセンスを設定してください。
