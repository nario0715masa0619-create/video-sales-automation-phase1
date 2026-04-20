$filePath = "send_email.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    # Line 131-141 を完全に削除（129-130 の空行の後から始まる重複）
    if ($i -ge 130 -and $i -le 140) {
        # スキップ
        continue
    }
    $newLines += $lines[$i]
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ 重複を完全に削除しました" -ForegroundColor Green
