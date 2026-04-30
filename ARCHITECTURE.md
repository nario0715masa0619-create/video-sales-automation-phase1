# フェーズ分割型アーキテクチャ設計書

## システム概要

営業自動化プロジェクトは「責任の分離」と「コスト効率」を重視した、段階的データ処理アーキテクチャを採用しています。

## フェーズ構成

### Phase 5: 生データ収集

役割: Webサイトからの情報抽出に特化

出力カラム:
- company_name
- website_url
- phone_number
- email
- source_page
- status
- scraped_at
- contact_form_url
- remarks

特徴: 検証ロジックを含まない、純粋なスクレイピング

利点: 処理速度が快適、エラーハンドリングがシンプル

### クレンジング層: データ精査

構成: bounce_checker.py + update_crm_emails.py

役割: 収集済みデータに対する外部サービス検証

処理内容:
- ZeroBounce APIによるメールバリデーション
- Catch-all判定とスコア80以上フィルタリング
- validation_status, validation_score を DB に追記

利点:
- APIクレジットを「確定されたデータのみ」に消費
- 後発の除外基準に対応可能
- 検証ロジックの独立性を維持

### メインCRM同期: 最終出力

役割: 検証済みデータをメインシートに反映

フィルター条件: Valid または スコア80以上のCatch-all のみ

出力: メインCRMシート（常にクリーン状態）
