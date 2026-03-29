"""
orchestrator.py
===============
全モジュールを統合するメイン処理スクリプト。
週次で自動実行されるワークフローと、
n8n / Make 連携用の Flask REST API を提供する。

【処理フロー（run_weekly_flow）】
  Step 1: 新規ターゲット候補を検索・スクレイピング
  Step 2: スコアリング実行
  Step 3: CRM 更新（UPSERT）
  Step 4: 送信対象リード抽出（A/Bランク・未送信 or 次の通数）
  Step 5: Gemini でメール文を生成
  Step 6: Gmail で送信
  Step 7: 送信結果を CRM に反映

【実行方法】
  ローカル: python orchestrator.py
  API経由:  POST /api/run   (Authorization: Bearer <API_SECRET_TOKEN>)
  Cloud:    Cloud Functions または Cloud Scheduler で週次実行
"""

import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from loguru import logger
from flask import Flask, request, jsonify
from flask_cors import CORS

import config
from target_scraper import (
    search_company_channels,
    get_channel_stats,
    filter_by_icp,
    ChannelData,
)
from scorer import score_channels, ScoredChannel
from crm_manager import (
    get_crm,
    upsert_lead,
    get_pending_leads,
    update_email_status,
    add_email_log,
    get_ng_list,
)
from email_generator import generate_email, EmailContent
from email_sender import GmailSender, SendResult, get_email_sender

# JST タイムゾーン
JST = timezone(timedelta(hours=9))

# ロギング設定
import os
os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
logger.remove()
logger.add(sys.stderr, level=config.LOG_LEVEL, format="{time:HH:mm:ss} | {level} | {message}")
logger.add(
    config.LOG_FILE,
    level=config.LOG_LEVEL,
    rotation="10 MB",
    retention="30 days",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)


# ==================================================
# データクラス定義
# ==================================================

@dataclass
class StepResult:
    """各ステップの実行結果"""
    step_name: str
    success: bool
    count: int = 0
    error_message: str = ""
    details: list[str] = field(default_factory=list)


@dataclass
class FlowResult:
    """週次フロー全体の実行結果"""
    started_at: datetime = field(default_factory=lambda: datetime.now(JST))
    finished_at: Optional[datetime] = None
    success: bool = False
    steps: list[StepResult] = field(default_factory=list)

    # 各ステップの統計
    channels_found: int = 0
    channels_passed_icp: int = 0
    leads_upserted: int = 0
    leads_pending: int = 0
    emails_generated: int = 0
    emails_sent: int = 0
    emails_bounced: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def duration_seconds(self) -> float:
        if self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return 0.0

    def to_summary(self) -> str:
        """実行結果のサマリー文字列を返す"""
        lines = [
            f"=== 週次フロー実行結果 [{self.started_at.strftime('%Y-%m-%d %H:%M')}] ===",
            f"ステータス: {'✅ 成功' if self.success else '❌ 失敗'}",
            f"実行時間: {self.duration_seconds:.0f}秒",
            "",
            "【スクレイピング】",
            f"  チャンネル候補数: {self.channels_found}件",
            f"  ICP通過数: {self.channels_passed_icp}件",
            f"  CRM更新数: {self.leads_upserted}件",
            "",
            "【メール送信】",
            f"  送信対象リード: {self.leads_pending}件",
            f"  メール生成数: {self.emails_generated}件",
            f"  送信成功数: {self.emails_sent}件",
            f"  バウンス数: {self.emails_bounced}件",
        ]
        if self.errors:
            lines.append("")
            lines.append("【エラー】")
            for err in self.errors[:5]:
                lines.append(f"  - {err}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """JSON レスポンス用の辞書を返す"""
        return {
            "success": self.success,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "duration_seconds": self.duration_seconds,
            "stats": {
                "channels_found": self.channels_found,
                "channels_passed_icp": self.channels_passed_icp,
                "leads_upserted": self.leads_upserted,
                "leads_pending": self.leads_pending,
                "emails_generated": self.emails_generated,
                "emails_sent": self.emails_sent,
                "emails_bounced": self.emails_bounced,
            },
            "errors": self.errors[:10],
        }


# ==================================================
# 週次フローの実装
# ==================================================

def _step1_scrape_targets(
    flow: FlowResult,
    keywords: list[str] | None = None
) -> list[ChannelData]:
    """
    Step 1: 新規ターゲット候補を検索・スクレイピングする。
    """
    step = StepResult(step_name="Step1: スクレイピング", success=False)
    logger.info("=== Step 1: ターゲット候補の検索・スクレイピング ===")

    try:
        # ✅ FIX 1: SERPAPI_KEY を環境変数から取得して引数として渡す
        serp_api_key = os.getenv('SERPAPI_KEY', '')
        if not serp_api_key:
            step.error_message = "SERPAPI_KEY が .env に設定されていません"
            logger.warning(step.error_message)
            flow.errors.append(f"Step1エラー: {step.error_message}")
            flow.steps.append(step)
            return []

        # 1-1. キーワード検索でチャンネルURLを収集
        # ✅ FIX 4: keywords が None の場合は config のデフォルトを使用
        if not keywords:
            keywords = config.DEFAULT_SEARCH_KEYWORDS
            logger.info(f"キーワード未指定のためデフォルトを使用: {keywords}")
        channel_urls = search_company_channels(keywords, serp_api_key)
        flow.channels_found = len(channel_urls)
        logger.info(f"チャンネル候補: {len(channel_urls)}件")

        if not channel_urls:
            step.error_message = "チャンネル候補が0件（SerpAPIキーを確認してください）"
            logger.warning(step.error_message)
            flow.steps.append(step)
            return []

        # 1-2. 各チャンネルの詳細データを取得
        channels = []
        for i, url in enumerate(channel_urls, 1):
            logger.info(f"チャンネル取得 [{i}/{len(channel_urls)}]: {url}")
            channel = get_channel_stats(url)
            # ✅ FIX 2: get_channel_stats が None を返す場合をスキップ
            if channel is not None:
                channels.append(channel)
            else:
                logger.warning(f"取得失敗（スキップ）: {url}")

            # レート制限対策（yt-dlp のブロック回避）
            time.sleep(config.SCRAPE_DELAY_SECONDS)

        # 1-3. ICP条件でフィルタリング
        # ✅ FIX 3: filter_by_icp はタプル (passed, rejected) を返すので正しくアンパック
        passed_channels, rejected_channels = filter_by_icp(channels)
        flow.channels_passed_icp = len(passed_channels)

        step.success = True
        step.count = len(passed_channels)
        logger.info(
            f"Step 1 完了: {len(passed_channels)}件がICP通過 "
            f"/ {len(rejected_channels)}件除外"
        )

    except Exception as e:
        step.error_message = str(e)
        flow.errors.append(f"Step1エラー: {e}")
        logger.error(f"Step 1 エラー: {traceback.format_exc()}")
        passed_channels = []

    flow.steps.append(step)
    return passed_channels


def _step2_3_score_and_upsert(
    flow: FlowResult,
    channels: list[ChannelData]
) -> list[ScoredChannel]:
    """
    Step 2+3: スコアリングと CRM 更新を一括実行する。
    """
    step = StepResult(step_name="Step2+3: スコアリング＆CRM更新", success=False)
    logger.info("=== Step 2+3: スコアリングと CRM 更新 ===")

    if not channels:
        step.error_message = "対象チャンネルが0件のためスキップ"
        logger.warning(step.error_message)
        flow.steps.append(step)
        return []

    try:
        # 2. スコアリング
        scored_channels = score_channels(channels)

        # 3. CRM に UPSERT
        upserted_count = 0
        for scored in scored_channels:
            crm_data = scored.to_crm_dict()
            try:
                upsert_lead(crm_data)
                upserted_count += 1
                time.sleep(5)  # Sheets API レート制限対策
            except Exception as e:
                logger.error(f"CRM更新エラー [{scored.channel_name}]: {e}")
                flow.errors.append(f"CRM更新エラー: {scored.channel_name} - {e}")

        flow.leads_upserted = upserted_count
        step.success = True
        step.count = upserted_count
        logger.info(f"Step 2+3 完了: {upserted_count}件をCRMに更新")

    except Exception as e:
        step.error_message = str(e)
        flow.errors.append(f"Step2+3エラー: {e}")
        logger.error(f"Step 2+3 エラー: {traceback.format_exc()}")
        scored_channels = []

    flow.steps.append(step)
    return scored_channels


def _step4_get_pending(flow: FlowResult) -> list[dict]:
    """
    Step 4: 送信対象リードを CRM から抽出する。
    """
    step = StepResult(step_name="Step4: 送信対象リード抽出", success=False)
    logger.info("=== Step 4: 送信対象リードの抽出 ===")

    try:
        # NGリストを取得
        ng_emails = set(get_ng_list())
        logger.info(f"NGリスト: {len(ng_emails)}件")

        # 送信対象リードを取得
        pending_leads = get_pending_leads(config.EMAIL_TARGET_RANKS)

        # NGリストに含まれるアドレスを除外
        filtered_leads = [
            lead for lead in pending_leads
            if lead.get("メールアドレス", "").lower() not in ng_emails
        ]

        # 1回の実行で送信する最大件数を制限
        limited_leads = filtered_leads[:config.EMAIL_MAX_SEND_PER_RUN]
        flow.leads_pending = len(limited_leads)

        step.success = True
        step.count = len(limited_leads)
        logger.info(
            f"Step 4 完了: {len(limited_leads)}件を送信対象として抽出 "
            f"（NGで {len(pending_leads) - len(filtered_leads)}件除外）"
        )

    except Exception as e:
        step.error_message = str(e)
        flow.errors.append(f"Step4エラー: {e}")
        logger.error(f"Step 4 エラー: {traceback.format_exc()}")
        limited_leads = []

    flow.steps.append(step)
    return limited_leads


def _step5_6_7_generate_and_send(
    flow: FlowResult,
    leads: list[dict],
    sender=None
) -> None:
    """
    Step 5+6+7: メール生成・送信・CRM反映を実行する。
    """
    step = StepResult(step_name="Step5+6+7: メール生成・送信・CRM反映", success=False)
    logger.info("=== Step 5+6+7: メール生成・送信・CRM反映 ===")

    if not leads:
        step.error_message = "送信対象リードが0件のためスキップ"
        logger.info(step.error_message)
        step.success = True
        flow.steps.append(step)
        return

    if sender is None:
        sender = GmailSender()

    for i, lead in enumerate(leads, 1):
        company_name = lead.get("会社名", "不明")
        email_address = lead.get("メールアドレス", "")
        channel_url = lead.get("チャンネルURL", "")

        # 送信通数の決定（現在の送信回数 + 1）
        current_count = int(lead.get("メール送信回数", 0) or 0)
        next_email_num = current_count + 1

        logger.info(
            f"処理中 [{i}/{len(leads)}]: {company_name} "
            f"({next_email_num}通目 / {email_address})"
        )

        # メールアドレスのバリデーション
        if not email_address or "@" not in email_address:
            logger.warning(f"メールアドレス未設定のためスキップ: {company_name}")
            flow.errors.append(f"メールアドレス未設定: {company_name}")
            continue

        # Step 5: メール文の生成
        email_content: Optional[EmailContent] = None
        try:
            email_content = generate_email(lead, next_email_num)
            flow.emails_generated += 1
        except Exception as e:
            logger.error(f"メール生成エラー [{company_name}]: {e}")
            flow.errors.append(f"メール生成エラー: {company_name} - {e}")
            continue

        # Step 6: メール送信
        send_result: Optional[SendResult] = None
        try:
            send_result = sender.send_email(
                to=email_address,
                subject=email_content.subject,
                body=email_content.body,
                company_name=company_name,
                email_count=next_email_num,
            )

            if send_result.success:
                flow.emails_sent += 1
                logger.info(f"送信成功: {company_name} ({next_email_num}通目)")
            else:
                logger.warning(f"送信失敗: {company_name} - {send_result.error_message}")
                if send_result.is_bounce:
                    flow.emails_bounced += 1

        except Exception as e:
            logger.error(f"送信エラー [{company_name}]: {e}")
            flow.errors.append(f"送信エラー: {company_name} - {e}")

        # Step 7: CRM への結果反映
        try:
            if send_result and send_result.success:
                update_email_status(channel_url, next_email_num, send_result.sent_at)
                add_email_log({
                    "会社名": company_name,
                    "メールアドレス": email_address,
                    "通数": next_email_num,
                    "件名": email_content.subject if email_content else "",
                    "送信結果": "成功",
                    "送信日時": (send_result.sent_at or datetime.now(JST)).strftime("%Y-%m-%d %H:%M:%S"),
                })

            elif send_result and send_result.is_bounce:
                crm = get_crm()
                crm.update_bounce_flag(channel_url)
                add_email_log({
                    "会社名": company_name,
                    "メールアドレス": email_address,
                    "通数": next_email_num,
                    "件名": email_content.subject if email_content else "",
                    "送信結果": "バウンス",
                    "エラー内容": send_result.error_message[:200],
                })

            elif send_result and not send_result.success:
                add_email_log({
                    "会社名": company_name,
                    "メールアドレス": email_address,
                    "通数": next_email_num,
                    "件名": email_content.subject if email_content else "",
                    "送信結果": "エラー",
                    "エラー内容": send_result.error_message[:200],
                })

        except Exception as e:
            logger.error(f"CRM反映エラー [{company_name}]: {e}")
            flow.errors.append(f"CRM反映エラー: {company_name} - {e}")

        time.sleep(2)

    step.success = True
    step.count = flow.emails_sent
    flow.steps.append(step)
    logger.info(
        f"Step 5+6+7 完了: "
        f"生成{flow.emails_generated}件 / "
        f"送信成功{flow.emails_sent}件 / "
        f"バウンス{flow.emails_bounced}件"
    )


# ==================================================
# メイン処理
# ==================================================

def run_weekly_flow(
    keywords: list[str] | None = None,
    skip_scraping: bool = False,
    dry_run: bool = False,
) -> FlowResult:
    """
    週次フローのメイン処理。
    """
    flow = FlowResult()
    logger.info("=" * 60)
    logger.info("週次フロー開始")
    logger.info(f"  skip_scraping: {skip_scraping}")
    logger.info(f"  dry_run: {dry_run}")
    logger.info("=" * 60)

    # 設定値の検証
    missing = config.validate_config()
    if missing:
        logger.warning(f"未設定の環境変数: {missing}")

    try:
        # Step 1〜3: スクレイピングが有効な場合のみ実行
        if not skip_scraping:
            channels = _step1_scrape_targets(flow, keywords)
            if channels:
                _step2_3_score_and_upsert(flow, channels)
        else:
            logger.info("スクレイピングをスキップ（既存CRMデータを使用）")

        # Step 4: 送信対象リードの抽出
        pending_leads = _step4_get_pending(flow)

        # Step 5+6+7: メール生成・送信・CRM反映
        if dry_run:
            logger.info(f"[DRY RUN] メール送信対象: {len(pending_leads)}件")
            for lead in pending_leads:
                current_count = int(lead.get("メール送信回数", 0) or 0)
                logger.info(
                    f"  [DRY RUN] {lead.get('会社名')} → "
                    f"{current_count + 1}通目 / {lead.get('メールアドレス')}"
                )
            flow.emails_generated = len(pending_leads)
        else:
            sender = get_email_sender("xserver")
            _step5_6_7_generate_and_send(flow, pending_leads, sender)

        flow.success = True

    except Exception as e:
        flow.success = False
        flow.errors.append(f"予期しないエラー: {e}")
        logger.error(f"フロー実行エラー: {traceback.format_exc()}")

    finally:
        flow.finished_at = datetime.now(JST)
        logger.info("\n" + flow.to_summary())

    return flow


# ==================================================
# Flask REST API（n8n / Make 連携用）
# ==================================================

app = Flask(__name__)
CORS(app)


def _verify_token(req) -> bool:
    """Bearer トークン認証"""
    auth_header = req.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False
    token = auth_header[7:]
    return token == config.API_SECRET_TOKEN


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now(JST).isoformat(),
        "version": "1.0.0",
    })


@app.route("/api/run", methods=["POST"])
def api_run():
    if not _verify_token(request):
        return jsonify({"error": "Unauthorized"}), 401

    body = request.get_json(silent=True) or {}
    skip_scraping = body.get("skip_scraping", False)
    dry_run = body.get("dry_run", False)
    keywords = body.get("keywords", None)

    logger.info(f"API経由でフロー実行: skip_scraping={skip_scraping}, dry_run={dry_run}")
    result = run_weekly_flow(keywords=keywords, skip_scraping=skip_scraping, dry_run=dry_run)
    return jsonify(result.to_dict()), 200 if result.success else 500


@app.route("/api/run-email-only", methods=["POST"])
def api_run_email_only():
    if not _verify_token(request):
        return jsonify({"error": "Unauthorized"}), 401

    body = request.get_json(silent=True) or {}
    dry_run = body.get("dry_run", False)

    result = run_weekly_flow(skip_scraping=True, dry_run=dry_run)
    return jsonify(result.to_dict()), 200 if result.success else 500


# ==================================================
# Cloud Functions エントリーポイント
# ==================================================

def cloud_function_entry(request=None):
    flow = run_weekly_flow()
    return (
        "success" if flow.success else "error",
        200 if flow.success else 500
    )


# ==================================================
# ローカル実行
# ==================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="動画スクレイピング×自動営業フロー オーケストレーター"
    )
    parser.add_argument(
        "--mode",
        choices=["run", "email-only", "api", "dry-run"],
        default="dry-run",
        help=(
            "run: フル実行 / "
            "email-only: メール送信のみ / "
            "api: Flask APIサーバー起動 / "
            "dry-run: 送信せずにログのみ（デフォルト）"
        ),
    )
    parser.add_argument(
        "--keywords",
        nargs="*",
        help="検索キーワード（スペース区切りで複数指定可）",
    )
    args = parser.parse_args()

    if args.mode == "api":
        logger.info(f"Flask API サーバーを起動します: port={config.FLASK_PORT}")
        app.run(host="0.0.0.0", port=config.FLASK_PORT, debug=False)

    elif args.mode == "run":
        result = run_weekly_flow(keywords=args.keywords)
        sys.exit(0 if result.success else 1)

    elif args.mode == "email-only":
        result = run_weekly_flow(skip_scraping=True)
        sys.exit(0 if result.success else 1)

    elif args.mode == "dry-run":
        logger.info("DRY RUN モード: メール送信は行いません")
        result = run_weekly_flow(dry_run=True)
        sys.exit(0 if result.success else 1)




