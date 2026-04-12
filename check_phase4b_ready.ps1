# Phase 4b 完成チェックリスト（large_scale_run.py 完了後）

Write-Host "=== Phase 4b 完成チェックリスト ===" -ForegroundColor Cyan

# 1. large_scale_run.py 完了確認
if (Test-Path "logs/large_scale_run_result.json") {
    Write-Host "✅ large_scale_run_result.json 生成完了" -ForegroundColor Green
    $results = Get-Content "logs/large_scale_run_result.json" -Encoding UTF8 | ConvertFrom-Json
    Write-Host "   - 総チャンネル数: $($results.summary.total_channels)"
    Write-Host "   - 総メール数: $($results.summary.total_emails)"
} else {
    Write-Host "❌ large_scale_run.py がまだ完了していません" -ForegroundColor Red
    exit 1
}

# 2. cache/email_data.json 確認
if (Test-Path "cache/email_data.json") {
    Write-Host "✅ cache/email_data.json 存在確認" -ForegroundColor Green
    $cacheData = Get-Content "cache/email_data.json" -Encoding UTF8 | ConvertFrom-Json
    $formOnly = @($cacheData.PSObject.Properties | Where-Object { $_.Value.form_url -and -not $_.Value.email }).Count
    Write-Host "   - フォーム URL あり＆メールなし: $formOnly 件（Step 6b テスト対象）" -ForegroundColor Yellow
} else {
    Write-Host "❌ cache/email_data.json が見つかりません" -ForegroundColor Red
    exit 1
}

# 3. test_step6b_production.py 実行準備
Write-Host ""
Write-Host "=== test_step6b_production.py 実行準備完了 ===" -ForegroundColor Green
Write-Host "以下のコマンドを実行してください:"
Write-Host "  python test_step6b_production.py" -ForegroundColor Cyan

# 4. 予想所要時間
Write-Host ""
Write-Host "予想所要時間: 10-15 分（$formOnly 件のフォーム送信テスト）"
