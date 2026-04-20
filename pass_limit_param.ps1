$filePath = "collect.py"
$content = Get-Content $filePath -Raw

# Line 254 を修正: limit を追加
$content = $content -replace "run_collect\(keywords=args\.keywords, dry_run=args\.dry_run\)", "run_collect(keywords=args.keywords, dry_run=args.dry_run, limit=args.limit)"

# Line 41 の関数定義も修正: limit パラメータを追加
$content = $content -replace "def run_collect\(keywords=None, dry_run=False, max_channels=150\):", "def run_collect(keywords=None, dry_run=False, max_channels=150, limit=None):"

$content | Set-Content $filePath -Encoding UTF8
Write-Host "✅ run_collect() に limit パラメータを追加しました" -ForegroundColor Green
