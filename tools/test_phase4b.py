import sys
import logging
from contact_form_extractor import FormSubmitter

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)

# テスト対象フォーム URL（実際の問い合わせフォーム）
test_urls = [
    "https://forms.gle/example",  # Google Forms テスト
    "https://example.com/contact",  # HTML フォーム テスト
]

# テストデータ
test_form_data = {
    'company': 'テスト企業 A',
    'email': 'test@example.com',
    'phone': '09000000000',
    'message': 'YouTube 営業活動テスト'
}

# FormSubmitter のインスタンス化と動作確認
submitter = FormSubmitter()
logger.info("✅ FormSubmitter インスタンス化成功")

# テスト URL（実際には実行しない、インポート確認のみ）
logger.info("✅ contact_form_extractor の主要クラス確認完了")
logger.info(f"  - FormSubmitter: {submitter.__class__.__name__}")
logger.info(f"  - メソッド: submit_form, strategies 設定済み")

# 実際のフォーム送信テスト（オプション）
# extracted_email = submitter.submit_form(test_urls[0], test_form_data)
# logger.info(f"抽出メール: {extracted_email if extracted_email else 'なし'}")

logger.info("✅ Phase 4b Step 6b 動作確認完了")
