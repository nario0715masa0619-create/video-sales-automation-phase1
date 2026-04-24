parts = [
    "# Video Sales Automation Phase 1～7\n\n**ステータス:** ✅ 完成\n",
    "## 概要\n\nYouTube 営業自動化パイプライン\n",
    "## フェーズ\n\nPhase 1～8 実装済み\n",
    "## セットアップ\n\npython -m venv venv\n",
    "## 使用方法\n\npython collect.py\n",
]

with open('README.md', 'w', encoding='utf-8') as f:
    f.writelines(parts)

print('✅ README.md 完成')
