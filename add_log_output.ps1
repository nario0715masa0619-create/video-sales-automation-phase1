$filePath = "send_email.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $newLines += $lines[$i]
    
    # Line 128 (continue の行) の後に logger.info を追加
    if ($i -gt 0 -and $lines[$i-1] -match "continue" -and $lines[$i] -match "^\s*$") {
        # 空行を見つけたら、その前に logger.info を挿入
        $newLines[-2] = $lines[$i-1]  # continue の行
        $newLines += ""
        $newLines += "            logger.info(f'[{processed_count}/{daily_limit}] {email_num} 通目を送信します: {ch_name}')"
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ ログ出力「通目を送信します」を追加しました" -ForegroundColor Green
