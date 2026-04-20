$filePath = "send_email.py"
$lines = @(Get-Content $filePath)

# Line 130 の重複を削除
$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    # Line 130 が Line 129 と同じなので削除
    if ($i -eq 129 -and $lines[$i] -match "if processed_count <= first_send_limit:" -and $newLines[-1] -match "if processed_count <= first_send_limit:") {
        # スキップ
        continue
    }
    $newLines += $lines[$i]
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ 重複行を削除しました" -ForegroundColor Green
