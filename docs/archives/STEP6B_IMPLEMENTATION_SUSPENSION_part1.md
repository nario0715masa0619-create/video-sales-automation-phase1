# collect.py Step 6b 実装見送りについて

## 概要
collect.py の Step 6b（フォーム自動送信でメール抽出）は、現在の実装では見送ることとしました。

## 理由
- contact_form_extractor モジュールの完成度が未成熟
- フォーム自動送信には複数のフレームワーク対応が必要（Google Forms、Formspree、Netlify Forms など）
- 実装コストが高く、現在のメール抽出手段（JSON-LD、mailto: リンク、正規表現）で基本的なニーズをカバーできている
- 優先度が低く、Phase 2 以降で実装予定

## 実装状況
現在のコード状態：
- Step 6b の処理はコメントアウトされている
- contact_form_extractor のインポート処理もコメントアウトされている
- エラーが発生しないよう try-except で保護されている

## 今後の実装予定
Phase 2 で以下を実装する予定：
1. contact_form_extractor モジュールの完成
2. 複数のフォームフレームワークへの対応
3. テスト実装と検証
4. collect.py Step 6b の本格導入

## 現在の Step 6 の構成
Step 6 はメールアドレス自動取得を行いますが、以下の優先度で実施：
1. Step 6a: email_extractor を使用した公式サイトからのメール抽出（実装済み・運用中）
2. Step 6b: フォーム自動送信でのメール抽出（見送り・コメントアウト中）

Step 6a で十分な成功率が得られるため、Step 6b の実装は優先度を低く設定しています。

