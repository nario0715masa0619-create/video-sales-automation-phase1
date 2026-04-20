$filePath = "README.md"
$content = Get-Content $filePath -Raw

$newSection = "

## 7. メールアドレス有効性チェック機能（2026-04-20 追加）

### 概要
メールアドレス抽出時に、ドメインの有効性を自動チェックする機能を実装。無効なドメイン（MXレコード未確認）のメールアドレスは CRM に保存されない。

### 実装内容
- 関数: is_valid_email(email) in email_extractor.py
  - 形式チェック
  - ドメイン実在確認: DNS MXレコード確認
- 依存パッケージ: dnspython

### テスト結果（2026-04-20）
- ✅ info@google.com: 有効
- ✅ support@microsoft.com: 有効
- ❌ xxx@xx.com: 無効
- ❌ aaaaa@bbbbb.com: 無効
- ❌ invalid-domain-12345.com: 無効

### 効果
- CRM 登録時の無効メールアドレス率を削減
- メール送信の失敗率低下
- 次フェーズ: company_info_extractor.py への統合
"

$content = $content + $newSection
$content | Set-Content $filePath -Encoding UTF8
Write-Host "✅ README.md を更新しました" -ForegroundColor Green
