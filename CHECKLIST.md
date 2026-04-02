# CHECKLIST.md - コミット前検証チェックリスト

## 概要
このドキュメントは、デグレード防止のため Step 6 と Step 7 の依存関係を検証するチェックリストです。
コード変更やテスト実行時に必ず確認してください。

---

## 重要: Step 6 と Step 7 の依存関係

**Step 7 → Step 6 の順序で実行する必要があります。逆順にするとメール情報が保存されません。**

### Step 7: メールアドレス抽出（先に実行）
- extractor.extract_email() でメール情報を取得
- ch.contact_email と ch.contact_form_url に設定

### Step 6: CRM 更新（後に実行）
- ch.to_crm_dict() でメール情報を含めて辞書化
- Google Sheets に保存

---

## コード変更時チェックリスト

### Step 6 または Step 7 を変更した場合
- [ ] Step 7 で ch.contact_email = email if email else '' が実行されているか確認
- [ ] Step 7 で ch.contact_form_url = contact_form_url if contact_form_url else '' が実行されているか確認
- [ ] Step 6 が Step 7 の後に実行されているか確認
- [ ] to_crm_dict() に メールアドレス と お問い合わせフォームURL が含まれているか確認

---

## ドライラン検証

実行コマンド: python collect.py --dry-run --keywords "テストキーワード"

確認項目:
- [ ] メール取得成功 が複数表示されている
- [ ] Step 7 完了 が表示されている
- [ ] Google Sheets のリード件数は変わっていない

---

## 本番実行検証

実行コマンド:
Remove-Item cache -Recurse -Force -ErrorAction SilentlyContinue
python collect.py

メール情報確認スクリプト実行後、確認項目:
- [ ] リード件数が増加している
- [ ] 最新10件のうち8件以上がメール情報を持つ

---

## コミット前チェックリスト（最終確認）

- [ ] ユニットテストがすべてパス
- [ ] ドライランにエラーがない
- [ ] 本番実行後、メール情報が Google Sheets に保存されている
- [ ] 最新10件のリードの80%以上がメール情報を持つ
- [ ] コミットメッセージに Step 6/7 の依存関係 を明記

---

## トラブルシューティング

### メール情報が保存されていない場合

1. Step の順序を確認
   - Step 7 が Step 6 より前にあるか確認

2. ch.contact_email への設定を確認
   - ch.contact_email = email if email else が実行されているか

3. to_crm_dict() でメール情報が含まれているか確認
   - メールアドレス: self.contact_email が含まれているか

---

## 参考資料

- デグレード原因: コミット 9a32169 で Step 7 の実装が変更され、メール設定処理が削除された
- 修正ポイント: Step 7 → Step 6 の順序、ch.contact_email への設定
- テストファイル: tests/test_collect_integration.py
