from crm_manager import CRMManager

crm = CRMManager()
leads = crm.get_all_leads()

# スコア別集計
print('スコア別集計:')
score_ranges = {
    'A (60+)': len([l for l in leads if l.get('総合スコア', 0) >= 60]),
    'B (40-59)': len([l for l in leads if 40 <= l.get('総合スコア', 0) < 60]),
    'C (20-39)': len([l for l in leads if 20 <= l.get('総合スコア', 0) < 40]),
    '低 (-20)': len([l for l in leads if l.get('総合スコア', 0) < 20]),
}
for range_name, count in score_ranges.items():
    print(f'  {range_name}: {count}件')

print(f'\n総数: {len(leads)}件')
