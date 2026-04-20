$filePath = "send_email.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    # Line 121-128 を全て削除して新しいロジックに置き換え
    if ($i -eq 120 -and $lines[$i] -match "# 1回目と2回目以降の切り替え判定") {
        $newLines += "            # 1回目と2回目以降の切り替え判定"
        $newLines += "            if processed_count <= first_send_limit:"
        $newLines += "                email_num = 1  # 1回目は必ず1通目"
        $newLines += "            else:"
        $newLines += "                # 2回目以降：データがあれば2通目、なければスキップ"
        $newLines += "                email_num = get_next_email_num(email)"
        $newLines += "                if not email_num:"
        $newLines += "                    logger.info(f'スキップ: 2通目データなし ({ch_name})')"
        $newLines += "                    continue"
        # 次の8行（121-128）をスキップ
        $i += 8
    } else {
        $newLines += $lines[$i]
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ 2回目以降は2通目データありの場合のみ送信するよう修正しました" -ForegroundColor Green
