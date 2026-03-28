"""
email_sender.py
===============
Gmail API 経由でメールを送信するモジュール。
将来の SendGrid 等への差し替えを想定した抽象クラス構造。

【設計方針】
- EmailSenderBase: 送信インターフェース（抽象クラス）
- GmailSender: Gmail API を使った実装
- SendGridSender: 将来の差し替え用プレースホルダ
- バウンス検出とフラグ管理を内包

【Gmail API 認証方法】
OAuth2 認証 (credentials.json → token.json) を使用する。
サービスアカウントでは Gmail 送信に制限があるため、
Gmail 送信には必ず OAuth2 認証を使うこと。
"""

import base64
import os
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from typing import Optional
from loguru import logger

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config

# JST タイムゾーン
JST = timezone(timedelta(hours=9))

# Gmail API スコープ（送信のみ）
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# バウンスエラーと見なす HTTP ステータスコード
BOUNCE_STATUS_CODES = [550, 551, 552, 553, 554]


# ==================================================
# ユーティリティ関数
# ==================================================

def _write_email_log(company_name: str, to: str, count: int, subject: str, body: str) -> None:
    """メール送信ログをファイルに記録する"""
    os.makedirs("logs", exist_ok=True)
    now_str = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    count_str = f"{count}通目" if count else "不明"
    company_str = company_name if company_name else "不明"
    
    log_content = f"""============================================================
[SEND] {now_str}
会社名: {company_str}
宛先: {to}
通数: {count_str}
件名: {subject}
本文:
{body}
"""
    with open("logs/email.log", "a", encoding="utf-8") as f:
        f.write(log_content)


# ==================================================
# データクラス定義
# ==================================================

@dataclass
class SendResult:
    """メール送信結果"""
    success: bool
    to_address: str
    subject: str
    message_id: str = ""
    sent_at: Optional[datetime] = None
    error_message: str = ""
    is_bounce: bool = False

    def __str__(self) -> str:
        status = "✅ 成功" if self.success else f"❌ 失敗（{self.error_message[:50]}）"
        return f"[送信結果] {self.to_address} → {status}"


# ==================================================
# 抽象基底クラス（インターフェース定義）
# ==================================================

class EmailSenderBase(ABC):
    """
    メール送信の抽象基底クラス。
    Gmail / SendGrid / Mailgun などへの差し替えはこのクラスを継承して実装する。
    """

    @abstractmethod
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_name: str = "",
        company_name: str = "",
        email_count: int = 0,
    ) -> SendResult:
        """
        メールを送信する。

        Args:
            to: 送信先メールアドレス
            subject: 件名
            body: 本文（プレーンテキスト）
            from_name: 送信者名（省略時は config.MY_NAME を使用）
            company_name: 企業名（ログ記録用）
            email_count: メール通数（ログ記録用）

        Returns:
            SendResult: 送信結果
        """
        pass

    @abstractmethod
    def check_connection(self) -> bool:
        """接続確認を行う"""
        pass


# ==================================================
# Gmail API 実装
# ==================================================

class GmailSender(EmailSenderBase):
    """
    Gmail API を使ったメール送信クラス。

    【認証フロー】
    1. 初回実行時: OAuth2 認証画面がブラウザで開く
    2. 認証後: config.GMAIL_OAUTH_TOKEN_FILE にトークンが保存される
    3. 2回目以降: 保存済みトークンを自動使用（有効期限切れ時は自動更新）

    【Gmail API の制限】
    - 1日の送信上限: 通常アカウント 500件/日
    - 大量送信の場合は Google Workspace（500〜2000件/日）を検討
    """

    def __init__(self):
        self._service = None
        self._credentials = None

    def _get_credentials(self) -> Credentials:
        """OAuth2 認証情報を取得（トークンのキャッシュと自動更新付き）"""
        token_file = config.GMAIL_OAUTH_TOKEN_FILE
        creds = None

        # 保存済みトークンの読み込み
        if os.path.exists(token_file):
            try:
                creds = Credentials.from_authorized_user_file(token_file, GMAIL_SCOPES)
            except Exception as e:
                logger.warning(f"トークンファイルの読み込みエラー: {e}")

        # トークンが無効または期限切れの場合は更新
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Gmail トークンを更新中...")
                creds.refresh(Request())
            else:
                # 初回認証（ブラウザが開く）
                # credentials.json は Google Cloud Console からダウンロード
                credentials_file = config.GOOGLE_SERVICE_ACCOUNT_JSON.replace(
                    "service_account.json", "oauth_credentials.json"
                )
                if not os.path.exists(credentials_file):
                    raise FileNotFoundError(
                        f"OAuth2 認証ファイルが見つかりません: {credentials_file}\n"
                        "Google Cloud Console から OAuth2 クライアント認証情報をダウンロードし、"
                        f"{credentials_file} に配置してください。"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, GMAIL_SCOPES
                )
                creds = flow.run_local_server(port=0)
                logger.info("Gmail OAuth2 認証完了")

            # トークンを保存
            os.makedirs(os.path.dirname(token_file), exist_ok=True)
            with open(token_file, "w") as f:
                f.write(creds.to_json())
            logger.info(f"Gmail トークンを保存しました: {token_file}")

        return creds

    def _get_service(self):
        """Gmail API サービスを取得（キャッシュ付き）"""
        if self._service is None:
            creds = self._get_credentials()
            self._service = build("gmail", "v1", credentials=creds)
        return self._service

    def _create_message(
        self,
        to: str,
        subject: str,
        body: str,
        from_name: str = "",
    ) -> dict:
        """
        Gmail API 用のメッセージオブジェクトを作成する。

        Args:
            to: 送信先アドレス
            subject: 件名
            body: 本文
            from_name: 送信者名

        Returns:
            dict: Gmail API 用のエンコード済みメッセージ
        """
        msg = MIMEMultipart("alternative")

        # ヘッダー設定
        sender_name = from_name or config.MY_NAME
        msg["From"] = f"{sender_name} <{config.GMAIL_SENDER_ADDRESS}>"
        msg["To"] = to
        msg["Subject"] = subject

        # スパムフィルタ対策のヘッダー
        msg["X-Mailer"] = "Python-Gmail-API"

        # 本文（プレーンテキスト）
        text_part = MIMEText(body, "plain", "utf-8")
        msg.attach(text_part)

        # Base64 エンコード
        encoded = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
        return {"raw": encoded}

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_name: str = "",
        company_name: str = "",
        email_count: int = 0,
    ) -> SendResult:
        """
        Gmail API を使ってメールを送信する。

        Args:
            to: 送信先メールアドレス
            subject: 件名
            body: 本文（プレーンテキスト）
            from_name: 送信者名
            company_name: 企業名（ログ記録用）
            email_count: メール通数（ログ記録用）

        Returns:
            SendResult: 送信結果
        """
        result = SendResult(
            success=False,
            to_address=to,
            subject=subject,
            sent_at=datetime.now(JST),
        )

        # 基本バリデーション
        if not to or "@" not in to:
            result.error_message = f"無効なメールアドレス: {to}"
            logger.error(result.error_message)
            return result

        # ログに保存
        _write_email_log(company_name, to, email_count, subject, body)

        try:
            service = self._get_service()
            message = self._create_message(to, subject, body, from_name)
            sent = service.users().messages().send(
                userId="me",
                body=message
            ).execute()

            result.success = True
            result.message_id = sent.get("id", "")
            logger.info(f"メール送信成功: {to} | MessageID: {result.message_id}")

        except HttpError as e:
            error_details = json.loads(e.content.decode()) if e.content else {}
            status_code = e.resp.status

            result.error_message = str(e)

            # バウンスの判定
            if status_code in BOUNCE_STATUS_CODES:
                result.is_bounce = True
                logger.warning(f"バウンス検出: {to} (HTTP {status_code})")
            else:
                logger.error(f"Gmail API エラー [{status_code}]: {to} - {e}")

        except FileNotFoundError as e:
            result.error_message = str(e)
            logger.error(f"認証ファイルエラー: {e}")

        except Exception as e:
            result.error_message = str(e)
            logger.error(f"メール送信エラー: {to} - {e}")

        return result

    def check_connection(self) -> bool:
        """Gmail API への接続確認"""
        try:
            service = self._get_service()
            # プロフィール情報を取得して接続確認
            profile = service.users().getProfile(userId="me").execute()
            logger.info(f"Gmail 接続確認OK: {profile.get('emailAddress')}")
            return True
        except Exception as e:
            logger.error(f"Gmail 接続確認失敗: {e}")
            return False


# ==================================================
# SendGrid 実装（将来の差し替え用プレースホルダ）
# ==================================================

class SendGridSender(EmailSenderBase):
    """
    【将来拡張用】SendGrid を使ったメール送信クラス。

    Gmail から SendGrid に切り替える場合の実装。
    大量送信（1日500件超）や配信率の向上が必要になった場合に切り替える。

    切り替え方法:
      orchestrator.py で
        sender = GmailSender()
      を
        sender = SendGridSender()
      に変えるだけで切り替え可能。

    必要な追加設定（.env）:
      SENDGRID_API_KEY=your_sendgrid_api_key
    """

    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "SENDGRID_API_KEY が未設定です。"
                ".env に SENDGRID_API_KEY を追加してください。"
            )

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_name: str = "",
        company_name: str = "",
        email_count: int = 0,
    ) -> SendResult:
        """
        SendGrid API を使ったメール送信。
        TODO: sendgrid パッケージのインストール後に実装
              pip install sendgrid
        """
        # ログに保存
        _write_email_log(company_name, to, email_count, subject, body)

        # TODO: SendGrid 実装
        raise NotImplementedError(
            "SendGrid 送信は未実装です。"
            "必要になった時点で実装してください。\n"
            "参考: https://docs.sendgrid.com/for-developers/sending-email/v3-python-code-example"
        )

    def check_connection(self) -> bool:
        raise NotImplementedError("SendGrid 接続確認は未実装です。")


# ==================================================
# Xserver SMTP 実装
# ==================================================

class XserverSMTPSender(EmailSenderBase):
    """
    Xserver SMTP を使ったメール送信クラス。
    
    【設定要件】
    以下の環境変数が必要です（.env）:
      SMTP_HOST=mail.xserver.jp
      SMTP_PORT=587
      SMTP_USER=your-email@example.com
      SMTP_PASSWORD=your-smtp-password
      MAIL_FROM=your-email@example.com
    """

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.mail_from = os.getenv("MAIL_FROM", self.smtp_user)

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_name: str = "",
        company_name: str = "",
        email_count: int = 0,
    ) -> SendResult:
        """
        Xserver SMTP を使ってメールを送信する。

        Args:
            to: 送信先メールアドレス
            subject: 件名
            body: 本文（プレーンテキスト）
            from_name: 送信者名
            company_name: 企業名（ログ記録用）
            email_count: メール通数（ログ記録用）

        Returns:
            SendResult: 送信結果
        """
        import smtplib

        result = SendResult(
            success=False,
            to_address=to,
            subject=subject,
            sent_at=datetime.now(JST),
        )

        # バリデーション
        if not to or "@" not in to:
            result.error_message = f"無効なメールアドレス: {to}"
            logger.error(result.error_message)
            return result

        if not self.smtp_host or not self.smtp_user or not self.smtp_password:
            result.error_message = "SMTP設定が不完全です（SMTP_HOST, SMTP_USER, SMTP_PASSWORD を確認）"
            logger.error(result.error_message)
            return result

        # ログに保存
        _write_email_log(company_name, to, email_count, subject, body)

        try:
            # メッセージの構築
            sender_name = from_name or config.MY_NAME
            msg = MIMEMultipart()
            
            # ✅ FIX: formataddr() を使用して From ヘッダーを正規化
            # これにより Gmail 等のメールサーバーが拒否しない形式に統一される
            msg["From"] = formataddr((str(Header(sender_name, 'utf-8')), self.mail_from))
            msg["To"] = to
            msg["Subject"] = Header(subject, "utf-8")
            msg.attach(MIMEText(body, "plain", "utf-8"))

            # SMTP 送信
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=20) as server:
                server.ehlo()
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.mail_from, to, msg.as_string())

            result.success = True
            logger.info(f"メール送信成功 (SMTP): {to}")

        except smtplib.SMTPAuthenticationError as e:
            result.error_message = f"SMTP認証失敗: {e}"
            logger.error(f"SMTP認証エラー [{to}]: {e}")

        except smtplib.SMTPException as e:
            result.error_message = f"SMTP エラー: {e}"
            logger.error(f"SMTP エラー [{to}]: {e}")

        except Exception as e:
            result.error_message = str(e)
            logger.error(f"メール送信エラー [{to}]: {e}")

        return result

    def check_connection(self) -> bool:
        """Xserver SMTP への接続確認"""
        import smtplib
        
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=20) as server:
                server.ehlo()
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
            logger.info("Xserver SMTP 接続確認OK")
            return True
        except Exception as e:
            logger.error(f"SMTP 接続確認失敗: {e}")
            return False


# ==================================================
# ファクトリ関数（プロバイダ選択）
# ==================================================

def get_email_sender(provider: str = "gmail") -> EmailSenderBase:
    """
    メール送信プロバイダを選択してインスタンスを返す。

    Args:
        provider: "gmail" / "sendgrid" / "xserver"

    Returns:
        EmailSenderBase: 指定したプロバイダの送信クラス

    Raises:
        ValueError: 未対応のプロバイダが指定された場合
    """
    providers = {
        "gmail": GmailSender,
        "sendgrid": SendGridSender,
        "xserver": XserverSMTPSender,
    }

    if provider not in providers:
        raise ValueError(
            f"未対応のプロバイダ: {provider}。"
            f"利用可能: {list(providers.keys())}"
        )

    return providers[provider]()


# ==================================================
# メイン処理（単体テスト用）
# ==================================================

if __name__ == "__main__":
    import sys

    logger.info("=== email_sender.py 単体テスト ===")

    # Gmail テスト
    try:
        logger.info("\n--- Gmail Sender テスト ---")
        sender = GmailSender()

        print("1. Gmail 接続確認...")
        if sender.check_connection():
            print("   → 接続OK")

            # テスト送信（オプション）
            if len(sys.argv) > 1 and sys.argv[1] == "--send-test":
                test_to = config.GMAIL_SENDER_ADDRESS
                print(f"2. テスト送信: {test_to}")
                result = sender.send_email(
                    to=test_to,
                    subject="【テスト】動画営業自動化システム 動作確認",
                    body="このメールはシステムの動作確認テストです。\n正常に受信できていれば設定は完了しています。",
                    company_name="テスト",
                    email_count=1,
                )
                print(f"   → {result}")
            else:
                print("2. テスト送信をスキップ（python email_sender.py --send-test で実行可能）")
        else:
            print("   → 接続失敗（認証設定を確認してください）")

    except Exception as e:
        logger.error(f"Gmail テスト失敗: {e}")

    # Xserver SMTP テスト（オプション）
    try:
        if os.getenv("SMTP_HOST"):
            logger.info("\n--- Xserver SMTP Sender テスト ---")
            xserver = XserverSMTPSender()
            print("3. SMTP 接続確認...")
            if xserver.check_connection():
                print("   → 接続OK")
            else:
                print("   → 接続失敗（SMTP設定を確認してください）")
    except Exception as e:
        logger.info(f"SMTP テストスキップ: {e}")
