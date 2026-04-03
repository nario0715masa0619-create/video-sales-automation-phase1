# 実装ログ

このファイルは、各機能実装の完了サマリーを記録します。

## 2026-04-02: API キーフェイルオーバー機能

**実装内容:**
- 複数 API キー（YOUTUBE_API_KEY, YOUTUBE_API_KEY2）のサポート
- 403 エラー時の自動キー切り替え
- キー別のクレジット使用状況追跡
- 詳細なログ出力（API KEY インデックス表示）

**完了項目:**
| 項目 | 状態 | コミット |
|------|------|---------|
| API キーフェイルオーバー基本機能 | ✅ | 5cb0c54 |
| キー別クレジット追跡 | ✅ | 1421ac1 |
| 詳細ログ出力 | ✅ | 1421ac1 |
| ユニットテスト | ✅ 3/3 合格 | 5cb0c54 |
| ドキュメント更新 | ✅ | 5cb0c54 |

**動作フロー:**
1. YOUTUBE_API_KEY1 で実行 → 通常動作
2. 403 Forbidden エラー → ログ: `403 Forbidden (API KEY 1)`
3. 自動切り替え → ログ: `別の API キーで再試行します (API KEY 2)`
4. YOUTUBE_API_KEY2 で再試行 → 成功時: `検索完了: ... (API KEY 2, クォータ消費: X pt)`
5. クレジット追跡 → `get_quota_status()` で `{API_KEY_1: X, API_KEY_2: Y}` を取得

**セキュリティ:**
- ✅ 実キーは `.env` に隠蔽
- ✅ ログには API KEY インデックスのみ記録
- ✅ `.env` は `.gitignore` で保護

**参考ファイル:**
- youtube_api_optimized.py: API キーフェイルオーバー実装
- tests/test_api_fallback.py: ユニットテスト
- DEVELOPMENT.md: セクション 7「API キーフェイルオーバー」

---

## 2026-04-02: Step 6/7 依存関係修正

**背景:** メールアドレスが Google Sheets に保存されない問題

**完了項目:**
- ✅ Step 7（メール抽出）を Step 6（CRM更新）より先に実行
- ✅ ch.contact_email と ch.contact_form_url 設定保証
- ✅ 自動検証関数 validate_crm_data_saved() 実装

**参考ファイル:**
- collect.py: Step 順序修正
- CHECKLIST.md: コミット前チェックリスト
- DEVELOPMENT.md: セクション 1-5

## 2026-04-02 (追記): API キーフェイルオーバー修正

**問題:** target_scraper.py で API キーがハードコードされていたため、API KEY 2 が読み込まれず、403 エラー時に切り替わらない

**修正内容:**
- target_scraper.py 14行目を修正
- YouTubeAPIOptimized(config.YOUTUBE_API_KEY, ...) → YouTubeAPIOptimized(api_key=None, ...)
- これにより .env から複数キーが正常に読み込まれるようになった

**結果:**
- ✅ API KEY 1 で 403 エラー → 自動的に API KEY 2 に切り替わる
- ✅ キー別クレジット追跡が機能
- ✅ ログに「API KEY 1」「API KEY 2」が正確に表示される
- ✅ テスト 3/3 合格

**コミット:** 0e0dde9


## 2026-04-03: Phase 1 実装完了

**実装内容:**
- YouTube チャンネル検索・フィルタリング・スコアリングパイプライン（Step 1-5）
- メール・公式サイト URL 自動抽出（Step 6-7）
- Google Sheets CRM への自動保存
- 複数 API キー（1-6）マネジメント

**実績:**
- チャンネル検索: 575 件
- フィルタリング: 222 件
- CRM 保存: 212 件
- 公式サイト URL: 212 件（100%）
- メール抽出: 36 件（17%）

**修正内容:**
- collect.py: Step 6-7 の if-else 構造修正、JSON マージロジック追加
- target_scraper.py: to_crm_dict() の getattr 削除（直接属性アクセス）
- email_extractor.py: リトライロジック追加（最大 3 回）
- テストモード廃止、全件処理に統一

**デバッグスクリプト整理:**
- tools/ ディレクトリに 300+ 本のデバッグスクリプトを集約

**コミット:** 63e9a38

---

**最終更新: 2026-04-03**
