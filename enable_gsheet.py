with open('website_scraper.py','r',encoding='utf-8') as f:
    lines = f.readlines()

# 151～158 行を有効化
modified = lines[:150]  # 150 行までコピー

# スプシ保存処理を追加（エラーハンドリング付き）
modified.append('        # Google Sheets に保存\n')
modified.append('        try:\n')
modified.append('            append_to_gsheet_phase5(\n')
modified.append('                result[\'company_name\'],\n')
modified.append('                result[\'phone_number\'],\n')
modified.append('                result[\'email\'],\n')
modified.append('                result[\'status\'],\n')
modified.append('                result[\'url\']\n')
modified.append('            )\n')
modified.append('            logger.info(f"✅ スプシ保存: {result[\'company_name\']}")\n')
modified.append('        except Exception as e:\n')
modified.append('            logger.error(f"❌ スプシ保存エラー: {e}")\n')
modified.append('\n')

# 159 行以降を追加
modified.extend(lines[158:])

with open('website_scraper.py','w',encoding='utf-8') as f:
    f.writelines(modified)

print('✅ スプシ保存処理を有効化しました')
