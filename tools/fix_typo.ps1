$filePath = "email_extractor.py"
$content = Get-Content $filePath -Raw

# タイポを修正
$content = $content -replace "import dns\.resolverquests", "import dns.resolver"

$content | Set-Content $filePath -Encoding UTF8
Write-Host "✅ dns.resolverquests → dns.resolver に修正しました" -ForegroundColor Green
