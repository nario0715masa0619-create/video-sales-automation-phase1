$filePath = "db_manager.py"
$lines = @(Get-Content $filePath)

Write-Host "=== get_send_history 関数（全体） ===" -ForegroundColor Cyan
$foundStart = $false
$lineCount = 0
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "def get_send_history") {
        $foundStart = $true
    }
    if ($foundStart) {
        Write-Host "$($i+1): $($lines[$i])"
        $lineCount++
        if ($lineCount -gt 25) {
            break
        }
    }
}
