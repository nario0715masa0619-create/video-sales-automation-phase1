$filePath = "send_email.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $newLines += $lines[$i]
    
    # Line 124: else: の直後に修正ロジックを挿入
    if ($i -eq 123 -and $lines[$i] -match "^\s*else:") {
        $newLines += "                # 2回目以降のデータを確認"
        $newLines += "                email_num = get_next_email_num(email)"
        $newLines += "                if not email_num:"
        $newLines += "                    # 2回目以降のデータがなければ、1通目を強制送信"
        $newLines += "                    email_num = 1"
        # 次の4行（125-128）をスキップ
        $i += 4
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ 2通目データなしの場合、1通目を強制送信するよう修正しました" -ForegroundColor Green
