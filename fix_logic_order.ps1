$filePath = "send_email.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    # Line 118-122 を削除して、新しいロジックに置き換え
    if ($i -ge 117 -and $i -le 121) {
        if ($i -eq 117) {
            # Line 118: "# 次に送るべき通数を判定" を削除
            $newLines += "            # スキップされなかった企業だけカウント"
            $newLines += "            processed_count += 1"
            $newLines += ""
            $newLines += "            # 1回目と2回目以降の切り替え判定"
            $newLines += "            if processed_count <= first_send_limit:"
            $newLines += "                email_num = 1  # 1回目は必ず1通目"
            $newLines += "            else:"
            $newLines += "                email_num = get_next_email_num(email)"
            $newLines += "                if not email_num:"
            $newLines += "                    logger.info(f'スキップ: 4通目以上で送信済み ({ch_name})')"
            $newLines += "                    continue"
        }
        # Line 119-122 をスキップ
    } else {
        $newLines += $lines[$i]
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ ロジック順序を修正しました（1回目強制→2回目判定）" -ForegroundColor Green
