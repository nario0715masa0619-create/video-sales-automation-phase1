$filePath = "email_extractor.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $newLines += $lines[$i]
    
    # Line 13 (dns.resolver の後) に import re を追加
    if ($i -eq 12 -and $lines[$i] -match "import dns.resolver") {
        $newLines += "import re"
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ import re をファイルの先頭に追加しました" -ForegroundColor Green

# 確認
Write-Host "
=== 確認: 先頭20行 ===" -ForegroundColor Cyan
$lines = @(Get-Content $filePath)
for ($i = 0; $i -lt 20; $i++) {
    Write-Host "$($i+1): $($lines[$i])"
}
