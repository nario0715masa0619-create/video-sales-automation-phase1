$filePath = "collect.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $newLines += $lines[$i]
    
    # Line 243 (--dry-run の add_argument の後) に --limit を追加
    if ($i -eq 242 -and $lines[$i] -match "^\s*\)$") {
        $newLines += "    parser.add_argument("
        $newLines += "        '--limit',"
        $newLines += "        type=int,"
        $newLines += "        default=None,"
        $newLines += "        help='処理対象リード数の上限（省略時はすべて処理）'"
        $newLines += "    )"
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ --limit オプションを追加しました" -ForegroundColor Green
