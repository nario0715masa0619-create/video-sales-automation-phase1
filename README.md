# Video Sales Automation - Phase 1

営業自動化プロジェクト Phase 1

## 主な機能
- CRM シートから企業 URL を読み込み
- ウェブサイトをクロール
- 電話番号とメールアドレスを自動抽出
- 結果を Phase 5 Google Sheet に保存

## 使用方法
python website_scraper.py
python website_scraper.py --limit=3

## Phase 5 Google Sheet スキーマ
列A: company_name (企業名)
列B: website_url (ウェブサイト URL)
列C: phone (電話番号または "None")
列D: email (メールアドレスまたは "None")
列E: source_page (抽出元ページ)
列F: status ("success" または "invalid")
列G: scraped_at (実行日時 YYYY-MM-DD HH:MM:SS)

## Email 抽出機能
tools/email_extractor.py で実装
優先順位: mailto リンク → JSON-LD → meta タグ → regex
ドメイン検証: テスト用ドメイン除外、誤字ドメイン除外
未検出時は "None" 文字列を保存

## パフォーマンス
1 URL あたり 10-30 秒
全 1,589 URL で約 4-8 時間（シングルスレッド）


## Phase 5 実行結果（2026-04-24 完了）

✅ **ミッション完了**

### 統計サマリー

| 項目 | 結果 |
|------|------|
| 入力 URL | 1,589 件 |
| 電話番号検出 | 866 件（67.4%） |
| invalid | 415 件 |
| skipped | 4 件 |
| 実行時間 | 約 7 時間 |
| 保存先 | Google Sheet Phase 5 + phase5_data.db |

### 処理内容

- ✅ 1,589 件の企業ウェブサイトをクロール
- ✅ 優先度順で電話番号を抽出（tel リンク → JSON‑LD → meta タグ → regex）
- ✅ メールアドレスも同様に抽出
- ✅ 866 件を phase5_data.db に永続化
- ✅ Google Sheet Phase 5 に同期完了
- ✅ ステータス「ready_to_contact」でマーク

### 成果物

- 📊 **Google Sheet Phase 5**：866 行
- 💾 **Database**：logs/phase5_data.db（866 レコード）
- 📝 **ログ**：logs/website_scraper.log
- 📚 **ドキュメント**：docs/ フォルダ（11 ファイル）



## Phase 6 準備中

### 役割

Phase 5 で抽出したメールアドレスを CRM Sheet に反映し、既営業企業の送信履歴をリセットするパイプラインです。

### 処理フロー

Phase 5 Google Sheet → crm_updater.py → CRM Sheet Leads
  ↓
Column C: メールアドレス上書き
Column Z: 送信回数リセット（Z>0 の場合）
Column AA～AE: 送信日時クリア（Z>0 の場合）

### マッチング方式

company_name + website_url の組合せで完全一致

### 処理内容

1. Phase 5 から有効メールを読込
2. CRM Leads と突合
3. 一致する企業のメールを上書き
4. Column Z を確認
   - Z == 0: 何もしない
   - Z > 0: Z を 0 にリセット & AA～AE をクリア
5. ログに記録

### 統計出力例

処理完了: 45 件
  ✅ 上書き: 40 件
    → うち リセット: 25 件
    → うち 上書きのみ: 15 件
  ⏭️  スキップ: 5 件（一致なし）
  ❌ エラー: 0 件

### 実行コマンド

python crm_updater.py

### ログ確認

Get-Content logs/phase6_crm_updater.log -Tail 50

### ドキュメント

- docs/PHASE6_PLAN.md
- docs/PHASE6_GUIDE.md

