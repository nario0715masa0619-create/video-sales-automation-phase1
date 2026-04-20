import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger
from config import ENABLE_AGGRESSIVE_MODE, AGGRESSIVE_BOUNCE_THRESHOLD

logger.add('logs/weekly_report.log', rotation='500 MB')

DB_PATH = Path("logs/send_log.db")

def generate_weekly_report():
    """週次レビュー：送信数、バウンス数、バウンス率を集計"""
    logger.info("=== 週次レビュー開始 ===")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 直近7日間のバウンスログを取得
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    
    c.execute("""
    SELECT 
        SUM(sent_count) as total_sent,
        SUM(bounce_count) as total_bounce,
        AVG(bounce_rate) as avg_bounce_rate
    FROM bounce_log
    WHERE date BETWEEN ? AND ?
    """, (seven_days_ago, today))
    
    result = c.fetchone()
    total_sent = result[0] or 0
    total_bounce = result[1] or 0
    avg_bounce_rate = result[2] or 0.0
    
    conn.close()
    
    logger.info(f"""
    ╔════════════════════════════════════════╗
    ║     週次レビュー（直近7日間）          ║
    ╚════════════════════════════════════════╝
    
    📊 送信数: {total_sent} 件
    📊 バウンス数: {total_bounce} 件
    📊 平均バウンス率: {avg_bounce_rate:.2f}%
    """)
    
    # 判定ロジック
    if avg_bounce_rate < 2.0:
        recommendation = "✅ 翌週 +5件/日に増やしてよい"
    elif avg_bounce_rate <= 5.0:
        recommendation = "⚠️  翌週は据え置き（増やさない）。リスト精査を検討"
    else:
        recommendation = "🔴 翌週は -5件/日に減らす。SMTP設定とリストをチェック"
    
    logger.info(f"判定: {recommendation}")
    
    # 4週目以降：aggressive mode の推奨判定
    if avg_bounce_rate < AGGRESSIVE_BOUNCE_THRESHOLD:
        if not ENABLE_AGGRESSIVE_MODE:
            logger.info(f"💡 Aggressive mode 推奨: バウンス率 {avg_bounce_rate:.2f}% < {AGGRESSIVE_BOUNCE_THRESHOLD}%")
            logger.info("config.py の ENABLE_AGGRESSIVE_MODE = True に設定することで、最大 30件/日を許可できます")
        else:
            logger.info("🚀 Aggressive mode が有効です（最大 30件/日）")
    else:
        if ENABLE_AGGRESSIVE_MODE:
            logger.warning("⚠️  バウンス率が上昇したため、Aggressive mode を無効化することを推奨します")
    
    return {
        "total_sent": total_sent,
        "total_bounce": total_bounce,
        "avg_bounce_rate": avg_bounce_rate,
        "recommendation": recommendation
    }

if __name__ == '__main__':
    report = generate_weekly_report()
