$filePath = "send_email.py"
$content = Get-Content $filePath -Raw
$lines = $content -split "
"

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $newLines += $lines[$i]
    
    # Line 126 (processed_count += 1) の直後に判定ロジックを追加
    if ($i -eq 125 -and $lines[$i] -match "processed_count") {
        $newLines += ""
        $newLines += "            # 1回目と2回目以降の切り替え判定"
        $newLines += "            if processed_count > first_send_limit:"
        $newLines += "                email_num = get_next_email_num(email)"
        $newLines += "                if not email_num:"
        $newLines += "                    logger.info(f'スキップ: 4通目以上で送信済み ({ch_name})')"
        $newLines += "                    continue"
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ 修正完了" -ForegroundColor Green
