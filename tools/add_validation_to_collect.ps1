$filePath = "collect.py"
$lines = @(Get-Content $filePath)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $newLines += $lines[$i]
    
    # Line 129 (get_email_from_youtube_channel の直後) に検証ロジックを追加
    if ($i -eq 128 -and $lines[$i] -match "get_email_from_youtube_channel") {
        # 次の10行をスキップしながら処理
        for ($j = 1; $j -le 10 -and $i + $j -lt $lines.Count; $j++) {
            $newLines += $lines[$i + $j]
            if ($lines[$i + $j] -match "contact_form_url if contact_form_url") {
                # Line 139 の後に検証ロジックを挿入
                $newLines += ""
                $newLines += "            # メールアドレスの有効性チェック"
                $newLines += "            if email:"
                $newLines += "                from email_extractor import is_valid_email"
                $newLines += "                if not is_valid_email(email):"
                $newLines += "                    logger.warning(f'無効なメール（ドメイン未確認）: {email} → スキップ')"
                $newLines += "                    email = None"
                break
            }
        }
        $i += 10
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ collect.py にメールアドレス検証ロジックを追加しました" -ForegroundColor Green
