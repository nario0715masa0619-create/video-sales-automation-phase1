$filePath = "db_manager.py"
$lines = @(Get-Content $filePath)

# Line 107 の "interval_days" を 0 に変更（テスト用）
$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "if days_since >= interval_days:") {
        $newLines += "        if days_since >= 0:  # テスト用：即座に送信可能"
    } else {
        $newLines += $lines[$i]
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ interval_days チェックを無効化しました（テスト用）" -ForegroundColor Green
