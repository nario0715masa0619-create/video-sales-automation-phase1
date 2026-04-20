$filePath = "send_email.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    # Line 129 の if 文を修正
    if ($i -eq 128 -and $lines[$i] -match "if processed_count > first_send_limit:") {
        # 1回目：email_num = 1 に固定
        $newLines += "            if processed_count <= first_send_limit:"
        $newLines += "                email_num = 1  # 1回目は必ず1通目"
        $newLines += "            else:"
        continue
    }
    
    # Line 130 以降をインデント調整
    if ($i -ge 129 -and $i -le 132) {
        if ($lines[$i] -match "^\s{16}") {
            # インデント20スペースを16スペースに調整（else ブロック内）
            $newLines += $lines[$i].Substring(4)
        } else {
            $newLines += $lines[$i]
        }
    } else {
        $newLines += $lines[$i]
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ 1回目/2回目の email_num 判定を修正しました" -ForegroundColor Green
