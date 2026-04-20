$filePath = "email_extractor.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    # Line 513: get_email_from_youtube_channel 関数内で、メール返却前に検証を追加
    if ($i -eq 512 -and $lines[$i] -match "def get_email_from_youtube_channel") {
        $newLines += $lines[$i]
        # 関数定義の後、戻り値を返す前に検証ロジックを挿入
        $i++
        while ($i -lt $lines.Count -and $lines[$i] -notmatch "return") {
            $newLines += $lines[$i]
            $i++
        }
        # return 文を修正
        if ($i -lt $lines.Count -and $lines[$i] -match "return") {
            $newLines += "    # メールアドレスの検証"
            $newLines += "    if email and not is_valid_email(email):"
            $newLines += "        logger.warning(f'無効なメールアドレス（ドメイン未確認）: {email}')"
            $newLines += "        email = None  # 無効なら None を返す"
            $newLines += "    "
            $newLines += $lines[$i]
        }
    } else {
        $newLines += $lines[$i]
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ get_email_from_youtube_channel 関数にメール検証を追加しました" -ForegroundColor Green
