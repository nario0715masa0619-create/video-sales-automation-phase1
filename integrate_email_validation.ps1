$filePath = "email_extractor.py"
$lines = @(Get-Content $filePath)
$newLines = @()

for ($i = 0; $i -lt $lines.Count; $i++) {
    $newLines += $lines[$i]
    
    # EXCLUDE_EMAIL_KEYWORDS チェックの直前に挿入
    if ($lines[$i] -match "# 譛邨ゅヵ繧｣繝ｫ繧ｿ繝ｪ繝ｳ繧ｰ.*EXCLUDE_EMAIL_KEYWORDS" -or $lines[$i] -match "# 最終フィルタリング.*EXCLUDE_EMAIL_KEYWORDS") {
        $newLines += "    # メールアドレスの有効性チェック（ドメイン実在確認）"
        $newLines += "    if email and not is_valid_email(email):"
        $newLines += "        logger.warning(f'無効なメール（ドメイン未確認）: {email} → スキップ')"
        $newLines += "        email = ''"
        $newLines += ""
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ メール有効性チェックを正しく挿入しました" -ForegroundColor Green
