$filePath = "collect.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $newLines += $lines[$i]
    
    # Line 69 (all_urls のログ出力の後) に limit フィルタを追加
    if ($i -eq 68 -and $lines[$i] -match "logger.info.*検索結果") {
        $newLines += ""
        $newLines += "    # limit オプションで件数制限"
        $newLines += "    if limit and len(all_urls) > limit:"
        $newLines += "        all_urls = all_urls[:limit]"
        $newLines += "        logger.info(f'📊 limit={limit} で制限しました（実際の処理対象: {len(all_urls)} 件）')"
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ limit オプションをロジックに統合しました" -ForegroundColor Green
