$filePath = "youtube_api_optimized.py"
$content = Get-Content $filePath -Raw

# Line 6 を修正
$content = $content -replace "from cache_manager import CacheManager", "from cache_manager import init_cache, get_cached_html, set_cached_html, clear_cache, get_cache_stats"

$content | Set-Content $filePath -Encoding UTF8
Write-Host "✅ youtube_api_optimized.py の import を修正しました（クラス → 関数）" -ForegroundColor Green
