## 13. 使用例

### パターン A: CRM から取得して Sheets に保存
from phone_extractor_crm import get_urls_from_crm
from phone_extractor_core import PhoneExtractor
from phone_sheet_saver import PhoneSheetSaver

urls = get_urls_from_crm(limit=50)
extractor = PhoneExtractor()
results = extractor.extract_batch([u["url"] for u in urls])
saver = PhoneSheetSaver()
saver.save(results)

### パターン B: Google 検索から取得して Sheets に保存
from phone_extractor_google import get_urls_from_google
from phone_extractor_core import PhoneExtractor
from phone_sheet_saver import PhoneSheetSaver

urls = get_urls_from_google("AI スタートアップ", num_results=20)
extractor = PhoneExtractor()
results = extractor.extract_batch([u["url"] for u in urls])
saver = PhoneSheetSaver()
saver.save(results)

### パターン C: CSV ファイルから読み込んで Sheets に保存
from phone_extractor_file import get_urls_from_file
from phone_extractor_core import PhoneExtractor
from phone_sheet_saver import PhoneSheetSaver

urls = get_urls_from_file("companies.csv")
extractor = PhoneExtractor()
results = extractor.extract_batch([u["url"] for u in urls])
saver = PhoneSheetSaver()
saver.save(results)

## 14. エラーハンドリング

| Status | 原因 | 対応 |
|--------|------|------|
| success | 全情報抽出成功 | 保存 |
| partial | 一部のみ抽出 | 保存（空欄あり） |
| not_found | 情報なし | 保存（なしと記録） |
| timeout | タイムアウト | リトライ 3 回 |
| forbidden | アクセス拒否 | スキップ、ログ |
| error | その他エラー | スキップ、詳細ログ |

## 15. キャッシング機能
- HTML キャッシュ: 24 時間有効
- キャッシュディレクトリ: cache/
- キャッシュキー: URL の SHA256 ハッシュ

## 16. リトライ機能
- タイムアウト: 3 回まで自動リトライ
- 待機時間: 2 秒（指数バックオフ）
- Forbidden: リトライなし

## 17. 実装優先度

### Phase 1（必須）
- phone_extractor_core.py（会社名・電話・メール抽出）
- phone_extractor_crm.py（CRM 連携）
- phone_sheet_saver.py（Sheets 保存）

### Phase 2（推奨）
- phone_extractor_google.py（Google 検索）
- phone_extractor_file.py（ファイル入出力）

### Phase 3（オプション）
- キャッシング強化
- バッチ処理最適化
- ローカル DB バックアップ機能
- 非同期処理対応

## 18. ファイル構成

ルート/
├── phone_extractor_core.py
├── phone_extractor_crm.py
├── phone_extractor_google.py
├── phone_extractor_file.py
├── phone_sheet_saver.py
├── cache/（キャッシュディレクトリ）
└── logs/（ログディレクトリ）
