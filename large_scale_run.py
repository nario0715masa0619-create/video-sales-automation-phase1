import sys
sys.path.insert(0, ".")
from collect import run_collect
from config import (
    CONSTRUCTION_KEYWORDS, RETAIL_KEYWORDS, FOOD_BEVERAGE_KEYWORDS,
    SERVICE_KEYWORDS, FINANCE_KEYWORDS, REAL_ESTATE_KEYWORDS,
    APPAREL_KEYWORDS, LOGISTICS_KEYWORDS
)
import os
import json
from datetime import datetime

genres = [
    ("建設", CONSTRUCTION_KEYWORDS),
    ("小売", RETAIL_KEYWORDS),
    ("飲食", FOOD_BEVERAGE_KEYWORDS),
    ("サービス", SERVICE_KEYWORDS),
    ("金融", FINANCE_KEYWORDS),
    ("不動産", REAL_ESTATE_KEYWORDS),
    ("アパレル", APPAREL_KEYWORDS),
    ("物流", LOGISTICS_KEYWORDS),
]

results = {}

for genre_name, keywords in genres:
    print("="*70)
    print(f"開始: {genre_name}ジャンル")
    print("="*70)
    
    if os.path.exists("cache/email_data.json"):
        os.remove("cache/email_data.json")
    
    try:
        run_collect(keywords=keywords, dry_run=False)
        
        if os.path.exists("cache/email_data.json"):
            with open("cache/email_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                with_email = sum(1 for d in data.values() if d.get("email"))
                results[genre_name] = {
                    "channels": len(data),
                    "emails": with_email,
                    "rate": round(with_email / len(data) * 100, 1) if data else 0
                }
                print(f"完了: {genre_name} {with_email}/{len(data)} 件 ({results[genre_name]['rate']}%)")
    except Exception as e:
        print(f"エラー: {genre_name} - {e}")
        results[genre_name] = {"error": str(e)}

print("="*70)
print("8ジャンル大規模実行完了")
print("="*70)
total_channels = sum(r.get("channels", 0) for r in results.values())
total_emails = sum(r.get("emails", 0) for r in results.values())
print(f"総チャンネル: {total_channels}")
print(f"総メール取得: {total_emails}")
if total_channels > 0:
    print(f"平均成功率: {round(total_emails/total_channels*100, 1)}%")

with open("logs/large_scale_run_result.json", "w", encoding="utf-8") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "total_channels": total_channels,
            "total_emails": total_emails,
            "average_rate": round(total_emails/total_channels*100, 1) if total_channels else 0
        }
    }, f, ensure_ascii=False, indent=2)

print("結果を logs/large_scale_run_result.json に保存しました")
