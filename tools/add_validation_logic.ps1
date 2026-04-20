$filePath = "email_extractor.py"
$lines = @(Get-Content $filePath)

$newLines = @()
$foundExtractFunc = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    # extract_email 関数内で、メールアドレスを返す前に検証を追加
    if ($line -match "return.*email" -and $foundExtractFunc) {
        $newLines += "    # メールアドレスの有効性チェック"
        $newLines += "    if is_valid_email(email):"
        $newLines += "        return email  # 有効なメールアドレス"
        $newLines += "    return None  # 無効なメールアドレス（ドメイン未確認）"
    } else {
        $newLines += $line
    }
    
    if ($line -match "def extract_email") {
        $foundExtractFunc = $true
    }
}

$newLines -join "
" | Set-Content $filePath -Encoding UTF8
Write-Host "✅ extract_email 関数に検証ロジックを追加しました" -ForegroundColor Green
