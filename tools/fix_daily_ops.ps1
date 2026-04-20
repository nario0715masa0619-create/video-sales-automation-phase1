$filePath = "daily_operations.py"
$content = Get-Content $filePath -Raw

# Line 26 の '--limit', '10' を '--limit', '15' に変更
$content = $content -replace "'--limit', '10'", "'--limit', '15'"

$content | Set-Content $filePath -Encoding UTF8
Write-Host "✅ daily_operations.py の --limit を 10 から 15 に変更しました" -ForegroundColor Green

# 確認
Get-Content $filePath | Select-String "send_email.py"
