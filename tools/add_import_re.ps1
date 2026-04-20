$filePath = "email_extractor.py"
$lines = @(Get-Content $filePath)

$newLines = @()
$hasImportRe = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "^import re") {
        $hasImportRe = $true
    }
    $newLines += $lines[$i]
}

# import re がなければ、最初の import の後に追加
if (-not $hasImportRe) {
    $newLines = @()
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "^import " -and $i -eq 0) {
            $newLines += "import re"
        }
        $newLines += $lines[$i]
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ import re を追加しました" -ForegroundColor Green
