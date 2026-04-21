## コード上の対応

### collect.py での処理

**現在の状態**
Step 6b の処理ブロック全体がコメントアウトされています。

**コード構造**

if contact_form_url:
    # ===== Step 6b: フォーム自動送信でメール抽出 =====
    # (未実装、スキップ)
    # try:
    #     import sys
    #     sys.path.insert(0, "tools")
    #     from contact_form_extractor import FormSubmitter
    #     submitter = FormSubmitter()
    #     form_data = {
    #         "company": company_name,
    #         "email": "test@example.com",
    #         "phone": "09000000000",
    #         "message": "YouTube 営業活動"
    #     }
    #     extracted_email = submitter.submit_form(
    #         contact_form_url,
    #         form_data
    #     )
    #     if extracted_email:
    #         email = extracted_email
    #         email_count += 1
    #         logger.info(
    #             f"✅ フォーム送信でメール抽出: "
    #             f"{company_name} → {email}"
    #         )
    #     else:
    #         logger.debug(
    #             f"フォーム送信: メール未抽出 {company_name}"
    #         )
    # except Exception as e:
    #     logger.warning(f"Step 6b エラー [{company_name}]: {e}")
else:
    logger.debug(f"メール取得失敗: {company_name}")

### 削除されたインポート

以下のインポートはコメントアウトされています：
- import sys
- sys.path.insert(0, "tools")
- from contact_form_extractor import FormSubmitter

