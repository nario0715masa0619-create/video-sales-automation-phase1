# === Phase 4 実装計画：collect.py への contact_form_extractor.py 統合 ===

## 現在の構造
Step 6: メールアドレス自動取得（line 116-149）
  → email_data[channel_url] = {"email": email, "website": website_url, "form_url": contact_form_url}
  → メール取得成功時のみ保存

## 統合案
Step 6a: メールアドレス自動取得（現在のまま）
Step 6b: フォーム自動送信（新規）
  → メール取得失敗した場合に実行
  → form_url が存在する場合のみ実行
  → Selenium で自動フォーム送信
  → メールアドレス抽出
  → email_data に "extracted_from_form": True を追記

## 実装フロー
1. import contact_form_extractor を collect.py に追加
2. Step 6 ループ内で：
   - if email取得成功 → Step 7 に進む
   - elif form_url存在 → Step 6b でフォーム送信実行
   - else → スキップ

## 予想効果
- メール取得失敗の 88 チャンネル中 73 チャンネルに対応
- メール検出率：17.0% → 85%+ 向上
- フォーム経由メール：70～90 件追加取得見込み

## 実装スケジュール
- Phase 4a: contact_form_extractor.py 完成（本日中 ← 現在地）
- Phase 4b: Step 6b 統合実装（明日）
- Phase 4c: テスト・デバッグ（2日）
- Phase 4d: 本番実行（3日目）
