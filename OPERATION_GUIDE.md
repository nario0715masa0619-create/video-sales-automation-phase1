# 本番稼働手順書

## 日次実行コマンド

### 1. 自動収集・CRM更新（毎日実行）
\\\powershell
cd D:\AI_スクリプト成果物\営業自動化プロジェクト\video-sales-automation-phase1
python src/collect.py
\\\

**処理内容：**
- YouTube検索（12キーワード）
- チャンネル詳細取得（550チャンネル程度）
- ICPフィルタリング
- 重複排除
- スコアリング（A/B/C ランク分類）
- メール抽出（公式サイトから）
- Google Sheets CRM自動更新

**出力：**
- logs/collect.log: 実行ログ
- cache/search_cache.json: 検索結果キャッシュ
- cache/scored_channels.pkl: スコアリング済みチャンネル
- Google Sheets: 194件のリード追加

**実行時間：** 約5～10分

---

### 2. メール送信（手動実行）
\\\powershell
python src/send_email.py
\\\

**処理内容：**
- Google Sheetsから未送信リードを取得
- メール本文生成（Gemini AI使用）
- 自動メール送信
- 送信履歴をGoogle Sheetsに記録

---

### 3. フォーム自動送信（手動実行）
\\\powershell
python src/form_submitter.py
\\\

**処理内容：**
- 問い合わせフォームへ自動入力・送信

---

## 定期メンテナンス

### キャッシュクリア（重い場合）
\\\powershell
Remove-Item cache -Recurse -Force
\\\

### Google Sheets クリア（リセット時）
\\\powershell
python -c "
import gspread
from google.oauth2.service_account import Credentials

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('credentials/service_account.json', scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open('SNS動画活用企業向け営業CRM管理シート').sheet1
sheet.batch_clear(['A2:ZZ10000'])
print('✅ クリア完了')
"
\\\

---

## トラブル時のデバッグ

### ログ確認
\\\powershell
Get-Content logs/collect.log -Tail 100
\\\

### キャッシュ状態確認
\\\powershell
Get-ChildItem cache
\\\

### Google Sheets 状態確認
\\\powershell
python tools/check_crm.py
\\\

---

## ファイル配置図

\\\
video-sales-automation-phase1/
├── src/
│   ├── collect.py ← 【これを実行】
│   ├── send_email.py ← メール送信用
│   ├── form_submitter.py ← フォーム送信用
│   ├── config.py
│   ├── target_scraper.py
│   ├── scorer.py
│   ├── crm_manager.py
│   ├── email_extractor.py
│   └── ...（その他メインコード）
├── scripts/
│   └── orchestrator.py （不使用）
├── tools/
│   ├── check_crm.py （デバッグ用）
│   ├── analyze_*.py （分析用）
│   └── ...（その他デバッグ用）
├── cache/
│   ├── search_cache.json （自動生成）
│   └── scored_channels.pkl （自動生成）
├── logs/
│   └── collect.log （実行ログ）
├── credentials/
│   └── service_account.json （Google認証）
└── PROJECT_STRUCTURE.md （このファイル）
\\\

---

## 実行前チェックリスト

- [ ] credentials/service_account.json が存在するか
- [ ] config.py に YOUTUBE_API_KEY が設定されているか
- [ ] config.py に GEMINI_API_KEY が設定されているか（メール送信時）
- [ ] Google Sheets シート名が正しいか
- [ ] インターネット接続は正常か

---

## 本番稼働スケジュール案

| 時間 | 処理 | コマンド |
|------|------|---------|
| 08:00 | 自動収集・CRM更新 | \python src/collect.py\ |
| 09:00 | メール送信 | \python src/send_email.py\ |
| 16:00 | ログ確認・メトリクス確認 | \Get-Content logs/collect.log -Tail 50\ |


---

## Phase 1 実行結果（2026-04-03）

### 初回本番実行

**実行コマンド:**
\\\ash
python collect.py
\\\

**実行結果:**
- YouTube 検索: 575 チャンネル取得（クォータ 12% 消費）
- ICP フィルタリング: 222 件合格
- 重複排除: 207 件
- スコアリング: 完了（A/B/C ランク分類）
- メール抽出: 36 件成功（17%）
- Google Sheets CRM 更新: 212 件新規追加

**実行時間:** 約 5～10 分

**出力ファイル:**
- logs/collect.log: 実行ログ
- cache/email_data.json: メール抽出結果（36 件）
- Google Sheets: リード 212 件

### 今後の運用

**日次実行:**
\\\ash
# キャッシュクリア & 本番実行
Remove-Item cache -Recurse -Force -ErrorAction SilentlyContinue
python collect.py
\\\

**ドライラン（テスト）:**
\\\ash
python collect.py --dry-run
\\\

---

**最終更新: 2026-04-03**
