"""
crm_manager.py
==============
Google Sheets（ミニCRM）との連携を管理するモジュール。

【シート構成】
  Sheet1: Leads        → 企業ごとのリード情報（メインCRM）
  Sheet2: メール送信ログ → 送信履歴の詳細ログ
  Sheet3: マスタ設定    → スコアリング設定・NGリスト等

【主な機能】
  - upsert_lead()     : リードの新規追加または更新（重複チェック込み）
  - get_pending_leads(): 送信対象リードの抽出
  - update_email_status(): メール送信後のステータス更新
  - add_email_log()   : 送信ログの追記
  - get_ng_list()     : NGリストの取得
"""

import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import gspread
from google.oauth2.service_account import Credentials

import config

# JST タイムゾーン
JST = timezone(timedelta(hours=9))

# Google API スコープ（Sheets 読み書き権限）
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

# ==================================================
# Leadsシートのカラム定義（列番号 ← 1始まり）
# ==================================================
# このマッピングを変更することでシート構造の変更に対応可能
LEADS_COLUMNS = {
    "会社名": 1,
    "担当者名": 2,
    "メールアドレス": 3,
    "問い合わせフォームURL": 4,
    "業種": 5,
    "規模（従業員数）": 6,         # 従業員数列
    "売上レンジ": 7,
    "地域": 8,
    "プラットフォーム種別": 9,     # プラットフォーム列
    "チャンネルURL": 10,
    "チャンネル名": 11,
    "最新動画タイトル": 12,
    "チャンネル登録者数": 13,
    "投稿数（直近3ヶ月）": 14,     # 直近3ヶ月投稿数列
    "平均再生数": 15,
    "平均エンゲージメント率": 16,
    "成長トレンド": 17,
    "投稿頻度スコア": 18,
    "再生数スコア": 19,
    "エンゲージメントスコア": 20,
    "トレンドスコア": 21,
    "総合スコア": 22,
    "ランク": 23,
    "営業ステータス": 24,
    "メール送信回数": 25,          # 送信回数列
    "1通目送信日": 26,
    "2通目送信日": 27,
    "3通目送信日": 28,
    "4通目送信日": 29,
    "最終送信日": 30,
    "開封フラグ": 31,
    "クリックフラグ": 32,
    "返信フラグ": 33,
    "バウンスフラグ": 34,
    "NGフラグ": 35,
    "備考": 36,
    "登録日": 37,
    "最終更新日": 38,
}

# メール送信ログシートのカラム定義
EMAIL_LOG_COLUMNS = {
    "ログID": 1,
    "会社名": 2,
    "メールアドレス": 3,
    "送信日時": 4,
    "通数": 5,
    "件名": 6,
    "送信結果": 7,
    "エラー内容": 8,
    "開封日時": 9,
    "クリック日時": 10,
    "備考": 11,
}

# 営業ステータスの定義
STATUS_UNTOUCHED = "未接触"
STATUS_IN_PROGRESS = "接触中"
STATUS_REPLIED = "返信あり"
STATUS_MEETING = "商談中"
STATUS_LOST = "失注"
STATUS_WON = "成約"
STATUS_NG = "NG"
STATUS_BOUNCE = "バウンス"


# ==================================================
# ユーティリティ関数
# ==================================================

def is_valid_email_for_send(email: str) -> bool:
    """送信対象のメールアドレスが有効かどうかを判定する"""
    if not email:
        return False
    e = email.strip()
    if e == "×取得失敗":
        return False
    if "@" not in e:
        return False
    return True


# ==================================================
# Google Sheets クライアント管理
# ==================================================

class CRMManager:
    """
    Google Sheets を使ったミニCRMの操作クラス。
    シングルトンパターンで接続を再利用する。
    """

    _instance: Optional["CRMManager"] = None
    _client: Optional[gspread.Client] = None
    _spreadsheet: Optional[gspread.Spreadsheet] = None

    def __new__(cls) -> "CRMManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _get_client(self) -> gspread.Client:
        """Google Sheets クライアントを取得（キャッシュ付き）"""
        if self._client is None:
            creds = Credentials.from_service_account_file(
                config.GOOGLE_SERVICE_ACCOUNT_JSON,
                scopes=SCOPES
            )
            self._client = gspread.authorize(creds)
            logger.info("Google Sheets クライアント初期化完了")
        return self._client

    def _get_spreadsheet(self) -> gspread.Spreadsheet:
        """スプレッドシートを取得（キャッシュ付き）"""
        if self._spreadsheet is None:
            client = self._get_client()
            self._spreadsheet = client.open_by_key(config.SPREADSHEET_ID)
            logger.info(f"スプレッドシート接続完了: {self._spreadsheet.title}")
        return self._spreadsheet

    def _get_sheet(self, sheet_name: str) -> gspread.Worksheet:
        """指定シートを取得"""
        return self._get_spreadsheet().worksheet(sheet_name)

    def _now_jst(self) -> str:
        """現在時刻（JST）を文字列で返す"""
        return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")

    def _date_jst(self) -> str:
        """今日の日付（JST）を文字列で返す"""
        return datetime.now(JST).strftime("%Y-%m-%d")

    # --------------------------------------------------
    # Leads シートの操作
    # --------------------------------------------------

    def get_all_leads(self) -> list[dict]:
        """
        Leads シートの全レコードを取得する。

        Returns:
            list[dict]: 全レコードの辞書リスト（ヘッダーをキーとして使用）
        """
        sheet = self._get_sheet(config.SHEET_LEADS)
        records = sheet.get_all_records()
        logger.debug(f"全リード取得: {len(records)}件")
        return records

    def find_lead_by_channel_url(self, channel_url: str) -> Optional[tuple[int, dict]]:
        """
        チャンネルURLでリードを検索する。

        Args:
            channel_url: 検索するチャンネルURL

        Returns:
            Optional[tuple[int, dict]]: (行番号, レコード辞書) または None
            ※ 行番号は 1始まり（ヘッダー行 = 1、データ1件目 = 2）
        """
        sheet = self._get_sheet(config.SHEET_LEADS)
        col_index = LEADS_COLUMNS["チャンネルURL"]

        try:
            cell = sheet.find(channel_url, in_column=col_index)
            if cell:
                row_data = sheet.row_values(cell.row)
                record = self._row_to_dict(row_data)
                return cell.row, record
        except gspread.exceptions.CellNotFound:
            pass
        return None

    def _row_to_dict(self, row_values: list) -> dict:
        """行データを辞書に変換"""
        result = {}
        for col_name, col_index in LEADS_COLUMNS.items():
            idx = col_index - 1  # 0始まりに変換
            result[col_name] = row_values[idx] if idx < len(row_values) else ""
        return result
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=5, max=30),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def upsert_lead(self, lead_data: dict) -> None:
        """
        リードを新規追加または更新する（重複チェック込み）。
        チャンネルURLを一意キーとして使用する。

        Args:
            lead_data: 保存するリードデータの辞書
                必須キー: "チャンネルURL"
                任意キー: LEADS_COLUMNS に定義された全項目
        """
        channel_url = lead_data.get("チャンネルURL", "")
        if not channel_url:
            logger.warning("チャンネルURLが未設定のためスキップ")
            return

        sheet = self._get_sheet(config.SHEET_LEADS)
        existing = self.find_lead_by_channel_url(channel_url)

        now = self._now_jst()
        today = self._date_jst()

        if existing:
            # 既存レコードの更新
            row_num, old_record = existing

            # 動的指標（スクレイピングで更新する項目）のみ更新
            update_fields = {
                "チャンネル登録者数": lead_data.get("チャンネル登録者数", old_record.get("チャンネル登録者数")),
                "投稿数（直近3ヶ月）": lead_data.get("投稿数（直近3ヶ月）", old_record.get("投稿数（直近3ヶ月）")),
                "平均再生数": lead_data.get("平均再生数", old_record.get("平均再生数")),
                "平均エンゲージメント率": lead_data.get("平均エンゲージメント率", old_record.get("平均エンゲージメント率")),
                "成長トレンド": lead_data.get("成長トレンド", old_record.get("成長トレンド")),
                "投稿頻度スコア": lead_data.get("投稿頻度スコア", old_record.get("投稿頻度スコア")),
                "再生数スコア": lead_data.get("再生数スコア", old_record.get("再生数スコア")),
                "エンゲージメントスコア": lead_data.get("エンゲージメントスコア", old_record.get("エンゲージメントスコア")),
                "トレンドスコア": lead_data.get("トレンドスコア", old_record.get("トレンドスコア")),
                "総合スコア": lead_data.get("総合スコア", old_record.get("総合スコア")),
                "ランク": lead_data.get("ランク", old_record.get("ランク")),
                "最新動画タイトル": lead_data.get("最新動画タイトル", old_record.get("最新動画タイトル", "")),
                "最終更新日": now,
            }

            # 各フィールドをセルに書き込む
            for col_name, value in update_fields.items():
                if col_name in LEADS_COLUMNS:
                    col_index = LEADS_COLUMNS[col_name]
                    sheet.update_cell(row_num, col_index, value)

            logger.info(f"リード更新: {lead_data.get('チャンネル名', channel_url)} (行{row_num})")

        else:
            # 新規レコードの追加
            row_data = [""] * len(LEADS_COLUMNS)

            # デフォルト値の設定
            defaults = {
                "営業ステータス": STATUS_UNTOUCHED,
                "メール送信回数": 0,
                "開封フラグ": "FALSE",
                "クリックフラグ": "FALSE",
                "返信フラグ": "FALSE",
                "バウンスフラグ": "FALSE",
                "NGフラグ": "FALSE",
                "プラットフォーム種別": "YouTube",
                "登録日": today,
                "最終更新日": now,
            }
            merged = {**defaults, **lead_data}

            for col_name, col_index in LEADS_COLUMNS.items():
                row_data[col_index - 1] = merged.get(col_name, "")

            sheet.append_row(row_data, value_input_option="USER_ENTERED")
            logger.info(f"リード新規追加: {lead_data.get('チャンネル名', channel_url)}")

        # API レート制限対策
        time.sleep(0.5)


    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=5, max=30),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def batch_upsert_leads(self, leads_data: list[dict]) -> None:
        """
        複数のリードを1回のAPI呼び出しでバッチ UPSERT する
        
        Args:
            leads_data: リード情報の辞書のリスト
        """
        if not leads_data:
            return
        
        logger.info(f"バッチ UPSERT 開始: {len(leads_data)}件")
        
        # 既存リードを取得
        existing_leads = self.get_all_leads()
        existing_urls = {lead.get('チャンネルURL', ''): idx for idx, lead in enumerate(existing_leads)}
        
        # 更新行と新規行を分離
        rows_to_update = []
        rows_to_append = []
        
        for lead_data in leads_data:
            channel_url = lead_data.get('チャンネルURL', '')
            if channel_url in existing_urls:
                row_idx = existing_urls[channel_url]
                rows_to_update.append((row_idx + 2, lead_data))  # +2はヘッダ + 1-index
            else:
                rows_to_append.append(lead_data)
        
        # 更新処理（バッチで実行）
        if rows_to_update:
            for row_idx, lead_data in rows_to_update:
                row_values = [lead_data.get(col, '') for col in self.LEADS_COLUMNS]
                self.worksheet.update_cell(row_idx, 1, row_values[0])
                for col_idx, val in enumerate(row_values[1:], 2):
                    self.worksheet.update_cell(row_idx, col_idx, val)
                time.sleep(0.5)  # セル更新間のスリープ
        
        # 新規追加処理
        if rows_to_append:
            for lead_data in rows_to_append:
                row_values = [lead_data.get(col, '') for col in self.LEADS_COLUMNS]
                self.worksheet.append_row(row_values)
                time.sleep(0.5)
        
        logger.info(f"バッチ UPSERT 完了: 更新{len(rows_to_update)}件、追加{len(rows_to_append)}件")
    def get_pending_leads(
        self,
        rank_filter: list[str] | None = None
    ) -> list[dict]:
        """
        メール送信対象のリードを抽出する。

        抽出条件:
        1. ランクが rank_filter に含まれる（デフォルト: config.EMAIL_TARGET_RANKS）
        2. NGフラグが FALSE であること
        3. バウンスフラグが FALSE であること
        4. 営業ステータスが "失注" / "成約" / "NG" でないこと
        5. 以下のいずれか:
           - メール送信回数 = 0（未接触）
           - 最終送信日から config.EMAIL_INTERVAL_DAYS 日以上経過 かつ
             送信回数 < config.EMAIL_MAX_SEQUENCE

        Args:
            rank_filter: 対象ランクのリスト（例: ["A", "B"]）

        Returns:
            list[dict]: 送信対象リードの辞書リスト
        """
        if rank_filter is None:
            rank_filter = config.EMAIL_TARGET_RANKS

        all_leads = self.get_all_leads()
        pending = []
        cutoff_date = datetime.now(JST) - timedelta(days=config.EMAIL_INTERVAL_DAYS)

        for lead in all_leads:
            # ランクフィルタ
            if lead.get("ランク") not in rank_filter:
                continue

            # NGフラグチェック
            if str(lead.get("NGフラグ", "FALSE")).upper() == "TRUE":
                continue

            # バウンスフラグチェック
            if str(lead.get("バウンスフラグ", "FALSE")).upper() == "TRUE":
                continue

            # 終了ステータスチェック
            status = lead.get("営業ステータス", "")
            if status in [STATUS_LOST, STATUS_WON, STATUS_NG, STATUS_BOUNCE]:
                continue

            # メールアドレスの有効性チェック
            email = str(lead.get("メールアドレス", ""))
            if not is_valid_email_for_send(email):
                continue

            # メール送信回数チェック
            email_count = int(lead.get("メール送信回数", 0) or 0)

            # 最大送信数に達している場合はスキップ
            if email_count >= config.EMAIL_MAX_SEQUENCE:
                continue

            # 未送信の場合は即対象
            if email_count == 0:
                pending.append(lead)
                continue

            # 最終送信日チェック（送信間隔以上経過しているか）
            last_sent_str = lead.get("最終送信日", "")
            if not last_sent_str:
                pending.append(lead)
                continue

            try:
                last_sent = datetime.strptime(
                    str(last_sent_str)[:19], "%Y-%m-%d %H:%M:%S"
                ).replace(tzinfo=JST)
                if last_sent <= cutoff_date:
                    pending.append(lead)
            except ValueError:
                # 日付パースエラー → 対象に含める
                logger.warning(f"最終送信日のパースエラー: {last_sent_str}")
                pending.append(lead)

        logger.info(f"送信対象リード: {len(pending)}件")
        return pending

    def update_email_status(
        self,
        channel_url: str,
        email_num: int,
        sent_at: Optional[datetime] = None
    ) -> bool:
        """
        メール送信後のステータスをCRMに更新する。

        Args:
            channel_url: 対象リードのチャンネルURL
            email_num: 送信した通数（1〜4）
            sent_at: 送信日時（Noneの場合は現在時刻）

        Returns:
            bool: 更新成功の場合 True
        """
        existing = self.find_lead_by_channel_url(channel_url)
        if not existing:
            logger.warning(f"リードが見つかりません: {channel_url}")
            return False

        row_num, _ = existing
        sheet = self._get_sheet(config.SHEET_LEADS)

        now_str = (sent_at or datetime.now(JST)).strftime("%Y-%m-%d %H:%M:%S")

        # 送信回数の更新
        sheet.update_cell(row_num, LEADS_COLUMNS["メール送信回数"], email_num)

        # 通数ごとの送信日を更新
        date_col_map = {
            1: "1通目送信日",
            2: "2通目送信日",
            3: "3通目送信日",
            4: "4通目送信日",
        }
        if email_num in date_col_map:
            col_name = date_col_map[email_num]
            sheet.update_cell(row_num, LEADS_COLUMNS[col_name], now_str)

        # 最終送信日の更新
        sheet.update_cell(row_num, LEADS_COLUMNS["最終送信日"], now_str)

        # 営業ステータスの更新
        sheet.update_cell(row_num, LEADS_COLUMNS["営業ステータス"], STATUS_IN_PROGRESS)

        # 最終更新日の更新
        sheet.update_cell(row_num, LEADS_COLUMNS["最終更新日"], self._now_jst())

        logger.info(f"メールステータス更新: {channel_url} → {email_num}通目送信済み")
        time.sleep(0.5)
        return True

    def update_bounce_flag(self, channel_url: str) -> bool:
        """
        バウンス（送信失敗）フラグを立てる。

        Args:
            channel_url: 対象リードのチャンネルURL

        Returns:
            bool: 更新成功の場合 True
        """
        existing = self.find_lead_by_channel_url(channel_url)
        if not existing:
            return False

        row_num, _ = existing
        sheet = self._get_sheet(config.SHEET_LEADS)
        sheet.update_cell(row_num, LEADS_COLUMNS["バウンスフラグ"], "TRUE")
        sheet.update_cell(row_num, LEADS_COLUMNS["営業ステータス"], STATUS_BOUNCE)
        sheet.update_cell(row_num, LEADS_COLUMNS["最終更新日"], self._now_jst())

        logger.warning(f"バウンスフラグ設定: {channel_url}")
        return True

    def set_ng_flag(self, channel_url: str) -> bool:
        """
        NG フラグを立てる（解除申請・クレーム等の場合に使用）。

        Args:
            channel_url: 対象リードのチャンネルURL

        Returns:
            bool: 更新成功の場合 True
        """
        existing = self.find_lead_by_channel_url(channel_url)
        if not existing:
            return False

        row_num, _ = existing
        sheet = self._get_sheet(config.SHEET_LEADS)
        sheet.update_cell(row_num, LEADS_COLUMNS["NGフラグ"], "TRUE")
        sheet.update_cell(row_num, LEADS_COLUMNS["営業ステータス"], STATUS_NG)
        sheet.update_cell(row_num, LEADS_COLUMNS["最終更新日"], self._now_jst())

        logger.info(f"NGフラグ設定: {channel_url}")
        return True

    # --------------------------------------------------
    # メール送信ログシートの操作
    # --------------------------------------------------

    def add_email_log(self, log_data: dict) -> None:
        """
        メール送信ログを記録する。

        Args:
            log_data: ログデータの辞書
                必須キー: 会社名、メールアドレス、通数、件名、送信結果
                任意キー: エラー内容、備考
        """
        sheet = self._get_sheet(config.SHEET_EMAIL_LOG)

        import uuid
        log_id = str(uuid.uuid4())[:8].upper()
        now_str = self._now_jst()

        row_data = [""] * len(EMAIL_LOG_COLUMNS)
        row_data[EMAIL_LOG_COLUMNS["ログID"] - 1] = log_id
        row_data[EMAIL_LOG_COLUMNS["会社名"] - 1] = log_data.get("会社名", "")
        row_data[EMAIL_LOG_COLUMNS["メールアドレス"] - 1] = log_data.get("メールアドレス", "")
        row_data[EMAIL_LOG_COLUMNS["送信日時"] - 1] = log_data.get("送信日時", now_str)
        row_data[EMAIL_LOG_COLUMNS["通数"] - 1] = log_data.get("通数", "")
        row_data[EMAIL_LOG_COLUMNS["件名"] - 1] = log_data.get("件名", "")
        row_data[EMAIL_LOG_COLUMNS["送信結果"] - 1] = log_data.get("送信結果", "")
        row_data[EMAIL_LOG_COLUMNS["エラー内容"] - 1] = log_data.get("エラー内容", "")
        row_data[EMAIL_LOG_COLUMNS["開封日時"] - 1] = log_data.get("開封日時", "")
        row_data[EMAIL_LOG_COLUMNS["クリック日時"] - 1] = log_data.get("クリック日時", "")
        row_data[EMAIL_LOG_COLUMNS["備考"] - 1] = log_data.get("備考", "")

        sheet.append_row(row_data, value_input_option="USER_ENTERED")
        logger.debug(f"送信ログ追記: {log_data.get('会社名')} - {log_data.get('通数')}通目")
        time.sleep(0.3)

    # --------------------------------------------------
    # マスタ設定シートの操作
    # --------------------------------------------------

    def get_ng_list(self) -> list[str]:
        """
        NGリスト（マスタ設定シート）からNGメールアドレスを取得する。

        Returns:
            list[str]: NGメールアドレスのリスト（小文字正規化済み）
        """
        try:
            sheet = self._get_sheet(config.SHEET_MASTER)
            all_values = sheet.get_all_values()

            ng_emails = []
            in_ng_section = False

            for row in all_values:
                if not row:
                    continue
                first_cell = str(row[0]).strip()

                # NGリストセクションの開始を検出
                if "NGリスト" in first_cell or "NG リスト" in first_cell:
                    in_ng_section = True
                    continue

                # 別セクションが始まったら終了
                if in_ng_section and first_cell and not first_cell.startswith("#"):
                    if "@" in first_cell:
                        ng_emails.append(first_cell.lower())
                    elif first_cell and first_cell != "メールアドレス":
                        # セクション区切りを検出
                        if len(first_cell) > 0 and "@" not in first_cell:
                            # メールアドレスでない行 = セクション終了
                            if in_ng_section and len(ng_emails) > 0:
                                break

            logger.debug(f"NGリスト取得: {len(ng_emails)}件")
            return ng_emails

        except Exception as e:
            logger.error(f"NGリスト取得エラー: {e}")
            return []


# ==================================================
# モジュール外から使いやすいショートカット関数
# ==================================================

_crm = None

def get_crm() -> CRMManager:
    """CRMManager のシングルトンインスタンスを返す"""
    global _crm
    if _crm is None:
        _crm = CRMManager()
    return _crm


def upsert_lead(lead_data: dict) -> None:
    """get_crm().upsert_lead() のショートカット"""
    get_crm().upsert_lead(lead_data)


def get_pending_leads(rank_filter: list[str] | None = None) -> list[dict]:
    """get_crm().get_pending_leads() のショートカット"""
    return get_crm().get_pending_leads(rank_filter)


def update_email_status(channel_url: str, email_num: int, sent_at=None) -> bool:
    """get_crm().update_email_status() のショートカット"""
    return get_crm().update_email_status(channel_url, email_num)


def add_email_log(log_data: dict) -> None:
    """get_crm().add_email_log() のショートカット"""
    get_crm().add_email_log(log_data)


def get_ng_list() -> list[str]:
    """get_crm().get_ng_list() のショートカット"""
    return get_crm().get_ng_list()


# ==================================================
# メイン処理（単体テスト用）
# ==================================================

if __name__ == "__main__":
    logger.info("=== crm_manager.py 単体テスト ===")
    logger.info("※ SPREADSHEET_ID と Google 認証設定が必要です")

    crm = get_crm()

    # テストリードを登録
    test_lead = {
        "会社名": "テスト株式会社",
        "チャンネルURL": "https://youtube.com/@test-company",
        "チャンネル名": "テストチャンネル",
        "チャンネル登録者数": 5000,
        "投稿数（直近3ヶ月）": 8,
        "平均再生数": 400,
        "平均エンゲージメント率": 3.2,
        "成長トレンド": "上昇",
        "総合スコア": 62.0,
        "ランク": "B",
        "メールアドレス": "test@test.co.jp",
    }

    print("1. リードの upsert テスト...")
    crm.upsert_lead(test_lead)
    print("   → 完了")

    print("2. 送信対象リードの取得テスト...")
    pending = crm.get_pending_leads()
    print(f"   → {len(pending)}件取得")

    print("3. NGリストの取得テスト...")
    ng_list = crm.get_ng_list()
    print(f"   → {len(ng_list)}件のNGアドレス")



