$filePath = "send_email.py"
$lines = @(Get-Content $filePath)

# Line 131-141 の重複ブロックを削除
$newLines = @()
$skipUntil = -1

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($i -lt $skipUntil) {
        continue
    }
    
    # Line 131 開始の重複ブロックを検出
    if ($i -eq 130 -and $lines[$i] -match "スキップされなかった企業だけカウント" -and $newLines[-1] -match "スキップされなかった企業だけカウント") {
        # Line 131-141 をスキップ（11行）
        $skipUntil = $i + 12
        continue
    }
    
    $newLines += $lines[$i]
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ 重複ブロック (Line 131-141) を削除しました" -ForegroundColor Green
