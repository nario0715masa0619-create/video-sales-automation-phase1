$filePath = "send_email.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($i -eq 128) {
        # Line 129-135 を正しくインデント付きで挿入
        $newLines += $lines[$i]  # "            # 1回目と2回目以降の切り替え判定"
        $newLines += "            if processed_count <= first_send_limit:"
        $newLines += "                email_num = 1  # 1回目は必ず1通目"
        $newLines += "            else:"
        $newLines += "                email_num = get_next_email_num(email)"
        $newLines += "                if not email_num:"
        $newLines += "                    logger.info(f'スキップ: 4通目以上で送信済み ({ch_name})')"
        $newLines += "                    continue"
        # 次の行 (134-135) をスキップ
        $i += 7
    } else {
        $newLines += $lines[$i]
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ インデント修正完了" -ForegroundColor Green
