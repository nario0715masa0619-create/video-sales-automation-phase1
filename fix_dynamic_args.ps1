$filePath = "daily_operations.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "import subprocess") {
        $newLines += $lines[$i]
        $newLines += "import sys"
    } elseif ($lines[$i] -match "def run_daily_operations\(\):") {
        $newLines += "def run_daily_operations(limit=15):"
    } elseif ($lines[$i] -match "'--limit', '15'") {
        $newLines += "        result = subprocess.run(['python', 'send_email.py', '--limit', str(limit)], check=True)"
    } elseif ($lines[$i] -match "if __name__") {
        $newLines += "if __name__ == '__main__':"
        $newLines += "    import sys"
        $newLines += "    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 15"
        $newLines += "    run_daily_operations(limit)"
        # 次の行をスキップ
        $i++
    } else {
        $newLines += $lines[$i]
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ daily_operations.py を動的引数対応に修正しました" -ForegroundColor Green
