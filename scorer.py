"""
scorer.py
=========
チャンネルデータを元にスコアリングを実行し、A/B/Cランクを付けるモジュール。

【スコアリング設計】
総合スコア（100点満点）= 以下4指標の合計
  - 投稿頻度スコア  （30点満点）
  - 再生数スコア    （25点満点）
  - エンゲージメントスコア（25点満点）
  - トレンドスコア  （20点満点）

【ランク基準】
  A: 70点以上  → 優先営業対象（即アクション）
  B: 40〜69点 → 準優先（スコアA が少ない週に対応）
  C: 39点以下 → 保留（今は対象外）

【修正履歴】
v2: target_scraper.py v3 との属性名不一致を修正
  - videos_3m_count  → recent_3m_count
  - trend_ratio（float）→ growth_trend（str）に対応
    "_growth_trend_to_ratio()" で文字列→数値変換
  - to_crm_dict の "成長トレンド" を growth_trend 文字列から直接取得
"""

from dataclasses import dataclass
from typing import Optional
from loguru import logger

from target_scraper import ChannelData
import config


# ==================================================
# データクラス定義
# ==================================================

@dataclass
class ScoredChannel:
    """スコアリング結果を保持するデータクラス"""
    channel: ChannelData

    # 各指標のスコア
    posting_frequency_score: float = 0.0   # 投稿頻度スコア（max 30）
    view_count_score: float = 0.0           # 再生数スコア（max 25）
    engagement_score: float = 0.0           # エンゲージメントスコア（max 25）
    trend_score: float = 0.0                # トレンドスコア（max 20）

    # 総合スコアとランク
    total_score: float = 0.0
    rank: str = "C"

    # スコア根拠（透明性のため）
    score_reason: str = ""

    @property
    def channel_name(self) -> str:
        return self.channel.channel_name

    @property
    def channel_url(self) -> str:
        return self.channel.channel_url

    def to_crm_dict(self) -> dict:
        """CRM（スプレッドシート）書き込み用の辞書を返す"""
        return {
            "会社名": self.channel_name,
            "担当者名": "",
            "メールアドレス": self.channel.contact_email,
            "問い合わせフォームURL": self.channel.contact_form_url,
            "業種": "",
            "規模（従業員数）": "",
            "売上レンジ": "",
            "地域": "",
            "プラットフォーム種別": "YouTube",
            "チャンネルURL": self.channel_url,
            "チャンネル名": self.channel_name,
            "チャンネル登録者数": self.channel.subscriber_count,
            # ✅ FIX 1: videos_3m_count → recent_3m_count
            "投稿数（直近3ヶ月）": self.channel.recent_3m_count,
            "平均再生数": round(self.channel.avg_view_count, 0),
            "平均エンゲージメント率": round(self.channel.avg_engagement_rate * 100, 2),
            # ✅ FIX 2: growth_trend は既に文字列ラベルなのでそのまま使用
            "成長トレンド": self.channel.growth_trend,
            "投稿頻度スコア": self.posting_frequency_score,
            "再生数スコア": self.view_count_score,
            "エンゲージメントスコア": self.engagement_score,
            "トレンドスコア": self.trend_score,
            "総合スコア": round(self.total_score, 1),
            "ランク": self.rank,
            "最新動画タイトル": self.channel.latest_video_title,
            "最新動画URL": self.channel.latest_video_url,
            "スコア根拠": self.score_reason,
        }


# ==================================================
# スコアリングロジック
# ==================================================

def _calc_threshold_score(value: float, thresholds: list[tuple[float, float]]) -> float:
    """
    しきい値リストに基づいてスコアを計算する汎用関数。

    Args:
        value: 評価対象の数値
        thresholds: [(しきい値, スコア)] のリスト（降順で記述すること）

    Returns:
        float: 該当するスコア（どのしきい値にも満たない場合は 0）
    """
    for threshold, score in thresholds:
        if value >= threshold:
            return float(score)
    return 0.0


def _growth_trend_to_ratio(growth_trend: str) -> float:
    """
    ✅ FIX 3: target_scraper v3 の growth_trend 文字列をスコア計算用の数値に変換。

    target_scraper.py v3 では trend_ratio（float）ではなく
    growth_trend（str）で成長傾向を保持しているため、
    スコア計算用に数値へ変換する。

    Args:
        growth_trend: "上昇" / "横ばい" / "やや下降" / "下降"

    Returns:
        float: トレンドスコア計算用の比率
    """
    mapping = {
        "上昇":     1.3,   # config.TREND_THRESHOLDS の 1.20 以上 → 満点
        "横ばい":   1.05,  # 1.00 以上 → 12点
        "やや下降": 0.85,  # 0.80 以上 → 6点
        "下降":     0.5,   # 0.80 未満 → 0点
    }
    return mapping.get(growth_trend, 1.0)


def _calc_posting_frequency_score(recent_3m_count: int) -> float:
    """
    投稿頻度スコアを計算する（最大30点）。

    直近3ヶ月の投稿本数に基づき算出。
    しきい値: config.POSTING_FREQ_THRESHOLDS で設定可能。

    Args:
        recent_3m_count: 直近3ヶ月の投稿本数

    Returns:
        float: 投稿頻度スコア（0〜30点）
    """
    return _calc_threshold_score(
        recent_3m_count,
        config.POSTING_FREQ_THRESHOLDS
    )


def _calc_view_count_score(avg_view_count: float, subscriber_count: int) -> float:
    """
    再生数スコアを計算する（最大25点）。

    「登録者比の再生率」（avg_view_count / subscriber_count）で評価。
    しきい値: config.VIEW_RATE_THRESHOLDS で設定可能。

    Args:
        avg_view_count: 直近3ヶ月の平均再生数
        subscriber_count: チャンネル登録者数

    Returns:
        float: 再生数スコア（0〜25点）
    """
    if subscriber_count <= 0:
        return 0.0

    view_rate = avg_view_count / subscriber_count
    return _calc_threshold_score(view_rate, config.VIEW_RATE_THRESHOLDS)


def _calc_engagement_score(avg_engagement_rate: float) -> float:
    """
    エンゲージメントスコアを計算する（最大25点）。

    しきい値: config.ENGAGEMENT_THRESHOLDS で設定可能。

    Args:
        avg_engagement_rate: 平均エンゲージメント率（0.0〜1.0）

    Returns:
        float: エンゲージメントスコア（0〜25点）
    """
    return _calc_threshold_score(
        avg_engagement_rate,
        config.ENGAGEMENT_THRESHOLDS
    )


def _calc_trend_score(trend_ratio: float) -> float:
    """
    トレンドスコアを計算する（最大20点）。

    Args:
        trend_ratio: トレンド比率（_growth_trend_to_ratio() で変換した値）

    Returns:
        float: トレンドスコア（0〜20点）
    """
    return _calc_threshold_score(trend_ratio, config.TREND_THRESHOLDS)


def assign_rank(score: float) -> str:
    """
    総合スコアからランク（A/B/C）を判定する。

    Args:
        score: 総合スコア（0〜100点）

    Returns:
        str: ランク文字列 "A" / "B" / "C"
    """
    if score >= config.RANK_A_MIN:
        return "A"
    elif score >= config.RANK_B_MIN:
        return "B"
    else:
        return "C"


def calculate_score(channel: ChannelData) -> ScoredChannel:
    """
    チャンネルデータを元にスコアリングを実行する。

    Args:
        channel: スコアリング対象のチャンネルデータ

    Returns:
        ScoredChannel: スコアリング結果
    """
    scored = ScoredChannel(channel=channel)

    # 各指標のスコアを計算
    # ✅ FIX 1: videos_3m_count → recent_3m_count
    scored.posting_frequency_score = _calc_posting_frequency_score(
        channel.recent_3m_count
    )
    scored.view_count_score = _calc_view_count_score(
        channel.avg_view_count,
        channel.subscriber_count
    )
    scored.engagement_score = _calc_engagement_score(
        channel.avg_engagement_rate
    )
    # ✅ FIX 3: trend_ratio → growth_trend 文字列を数値に変換してから計算
    scored.trend_score = _calc_trend_score(
        _growth_trend_to_ratio(channel.growth_trend)
    )

    # 総合スコアの計算
    scored.total_score = (
        scored.posting_frequency_score
        + scored.view_count_score
        + scored.engagement_score
        + scored.trend_score
    )

    # ランク判定
    scored.rank = assign_rank(scored.total_score)

    # スコア根拠の文字列生成（CRM保存・デバッグ用）
    scored.score_reason = (
        f"投稿頻度:{scored.posting_frequency_score:.0f}/"
        f"{config.SCORE_WEIGHTS['posting_frequency']} "
        f"再生数:{scored.view_count_score:.0f}/"
        f"{config.SCORE_WEIGHTS['view_count']} "
        f"エンゲージ:{scored.engagement_score:.0f}/"
        f"{config.SCORE_WEIGHTS['engagement']} "
        f"トレンド:{scored.trend_score:.0f}/"
        f"{config.SCORE_WEIGHTS['trend']} "
        f"→ 合計{scored.total_score:.1f}点({scored.rank}ランク)"
    )

    logger.debug(
        f"{channel.channel_name}: {scored.score_reason}"
    )

    return scored


def score_channels(channels: list[ChannelData]) -> list[ScoredChannel]:
    """
    チャンネルリストを一括スコアリングし、スコア降順で返す。

    Args:
        channels: スコアリング対象のチャンネルリスト

    Returns:
        list[ScoredChannel]: スコア降順に並んだ結果リスト
    """
    scored_list = []

    for channel in channels:
        scored = calculate_score(channel)
        scored_list.append(scored)

    # スコア降順でソート
    scored_list.sort(key=lambda x: x.total_score, reverse=True)

    # ランク別の集計ログ
    rank_counts = {"A": 0, "B": 0, "C": 0}
    for s in scored_list:
        rank_counts[s.rank] = rank_counts.get(s.rank, 0) + 1

    logger.info(
        f"スコアリング完了: "
        f"Aランク {rank_counts['A']}件 / "
        f"Bランク {rank_counts['B']}件 / "
        f"Cランク {rank_counts['C']}件"
    )

    return scored_list


# ==================================================
# メイン処理（単体テスト用）
# ==================================================

if __name__ == "__main__":
    from dataclasses import asdict

    logger.info("=== scorer.py 単体テスト ===")

    # テストデータ作成（✅ FIX: フィールド名を target_scraper v3 に合わせる）
    test_cases = [
        # Aランク相当: 積極投稿・高エンゲージ・成長中
        ChannelData(
            channel_url="https://youtube.com/@test-a",
            channel_name="テストA社",
            subscriber_count=10_000,
            recent_3m_count=15,          # ✅ videos_3m_count → recent_3m_count
            avg_view_count=1_500,
            avg_engagement_rate=0.06,
            growth_trend="上昇",          # ✅ trend_ratio → growth_trend（文字列）
        ),
        # Bランク相当: 普通の投稿・平均的なエンゲージ
        ChannelData(
            channel_url="https://youtube.com/@test-b",
            channel_name="テストB社",
            subscriber_count=5_000,
            recent_3m_count=6,
            avg_view_count=200,
            avg_engagement_rate=0.02,
            growth_trend="横ばい",
        ),
        # Cランク相当: 少ない投稿・低エンゲージ・下降傾向
        ChannelData(
            channel_url="https://youtube.com/@test-c",
            channel_name="テストC社",
            subscriber_count=2_000,
            recent_3m_count=3,
            avg_view_count=30,
            avg_engagement_rate=0.005,
            growth_trend="下降",
        ),
    ]

    results = score_channels(test_cases)

    print("\n--- スコアリング結果 ---")
    for r in results:
        print(f"\n【{r.rank}ランク】{r.channel_name}")
        print(f"  総合スコア: {r.total_score:.1f}点")
        print(f"  根拠: {r.score_reason}")


