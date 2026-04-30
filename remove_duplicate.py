with open('website_scraper.py','r',encoding='utf-8') as f:
    lines = f.readlines()

# 139～141 行の古いコードを削除
modified = lines[:138] + lines[141:]

with open('website_scraper.py','w',encoding='utf-8') as f:
    f.writelines(modified)

print('✅ 重複コードを削除しました')
