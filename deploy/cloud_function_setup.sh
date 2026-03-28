#!/bin/bash
# =====================================================
# deploy/cloud_function_setup.sh
# Google Cloud Functions へのデプロイスクリプト
# =====================================================
# 使用方法:
#   chmod +x deploy/cloud_function_setup.sh
#   ./deploy/cloud_function_setup.sh
#
# 前提条件:
#   - gcloud CLI がインストール・ログイン済みであること
#   - GCP プロジェクトが作成済みであること
#   - 請求先アカウントが設定済みであること
# =====================================================

set -euo pipefail  # エラー時に即座に停止

# =====================================================
# 設定値（必要に応じて変更してください）
# =====================================================

# GCP プロジェクト ID（変更必須）
GCP_PROJECT_ID="your-gcp-project-id"

# デプロイするリージョン（日本に近いリージョン推奨）
REGION="asia-northeast1"  # 東京

# Cloud Functions の関数名
FUNCTION_NAME="video-sales-weekly-flow"

# Cloud Scheduler のジョブ名
SCHEDULER_JOB_NAME="video-sales-weekly-trigger"

# 週次実行のスケジュール（毎週月曜日 AM9:00 JST）
# cron形式: 分 時 日 月 曜日
SCHEDULE="0 9 * * 1"
TIMEZONE="Asia/Tokyo"

# Cloud Functions のメモリ・タイムアウト設定
MEMORY="512MB"
TIMEOUT="540s"  # 最大9分（スクレイピングに時間がかかるため）
RUNTIME="python312"

# =====================================================
# カラー出力ユーティリティ
# =====================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# =====================================================
# 事前チェック
# =====================================================

info "デプロイ前チェックを開始します..."

# gcloud CLI の確認
if ! command -v gcloud &> /dev/null; then
    error "gcloud CLI がインストールされていません。\nhttps://cloud.google.com/sdk/docs/install からインストールしてください。"
fi

# ログイン確認
CURRENT_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null)
if [ -z "$CURRENT_ACCOUNT" ]; then
    error "gcloud にログインしていません。\n'gcloud auth login' を実行してください。"
fi
info "gcloud アカウント: $CURRENT_ACCOUNT"

# プロジェクトの設定
gcloud config set project "$GCP_PROJECT_ID" || error "プロジェクト '$GCP_PROJECT_ID' の設定に失敗しました。"
success "プロジェクト設定: $GCP_PROJECT_ID"

# .env ファイルの確認
if [ ! -f ".env" ]; then
    error ".env ファイルが見つかりません。.env.example をコピーして設定してください。"
fi
success ".env ファイル確認OK"

# credentials フォルダの確認
if [ ! -d "credentials" ]; then
    warn "credentials/ フォルダが見つかりません。サービスアカウントキーを配置してください。"
fi

# =====================================================
# Step 1: 必要な API を有効化
# =====================================================

info "必要な Google Cloud API を有効化中..."

gcloud services enable cloudfunctions.googleapis.com --quiet
gcloud services enable cloudscheduler.googleapis.com --quiet
gcloud services enable sheets.googleapis.com --quiet
gcloud services enable gmail.googleapis.com --quiet
gcloud services enable generativelanguage.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet

success "API 有効化完了"

# =====================================================
# Step 2: Secret Manager に環境変数を登録（推奨）
# =====================================================

info "Secret Manager を有効化中..."
gcloud services enable secretmanager.googleapis.com --quiet

# .env の内容を Secret Manager に登録する場合（セキュリティ強化）
# 本番環境ではこちらを推奨
if [ "${USE_SECRET_MANAGER:-false}" = "true" ]; then
    info ".env の内容を Secret Manager に登録中..."

    while IFS='=' read -r key value; do
        # コメント行とブランク行をスキップ
        [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
        # 値を Secret Manager に登録
        echo -n "$value" | gcloud secrets create "$key" --data-file=- --replication-policy=automatic 2>/dev/null || \
        echo -n "$value" | gcloud secrets versions add "$key" --data-file=- 2>/dev/null
    done < .env

    success "Secret Manager への登録完了"
else
    warn "Secret Manager の使用はスキップ（USE_SECRET_MANAGER=true で有効化可能）"
fi

# =====================================================
# Step 3: Cloud Functions にデプロイ
# =====================================================

info "Cloud Functions にデプロイ中（数分かかります）..."

# .env の値を環境変数として Cloud Functions に渡す
ENV_VARS=""
while IFS='=' read -r key value; do
    [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
    # 改行・スペースを除去
    value=$(echo "$value" | tr -d '\n\r')
    ENV_VARS="${ENV_VARS},${key}=${value}"
done < .env
ENV_VARS="${ENV_VARS:1}"  # 先頭のカンマを除去

gcloud functions deploy "$FUNCTION_NAME" \
    --gen2 \
    --runtime="$RUNTIME" \
    --region="$REGION" \
    --source="." \
    --entry-point="cloud_function_entry" \
    --trigger-http \
    --allow-unauthenticated=false \
    --memory="$MEMORY" \
    --timeout="$TIMEOUT" \
    --set-env-vars="$ENV_VARS" \
    --min-instances=0 \
    --max-instances=1 \
    --quiet

# デプロイされた関数の URL を取得
FUNCTION_URL=$(gcloud functions describe "$FUNCTION_NAME" \
    --region="$REGION" \
    --format="value(serviceConfig.uri)" 2>/dev/null)

if [ -z "$FUNCTION_URL" ]; then
    # gen2 でない場合のフォールバック
    FUNCTION_URL=$(gcloud functions describe "$FUNCTION_NAME" \
        --region="$REGION" \
        --format="value(httpsTrigger.url)" 2>/dev/null)
fi

success "Cloud Functions デプロイ完了"
info "関数 URL: $FUNCTION_URL"

# =====================================================
# Step 4: Cloud Scheduler の設定（週次トリガー）
# =====================================================

info "Cloud Scheduler を設定中..."

# サービスアカウントの取得（Cloud Functions 呼び出し用）
PROJECT_NUMBER=$(gcloud projects describe "$GCP_PROJECT_ID" --format="value(projectNumber)")
SERVICE_ACCOUNT="service-${PROJECT_NUMBER}@gcf-admin-robot.iam.gserviceaccount.com"

# 既存のジョブがある場合は削除して再作成
if gcloud scheduler jobs describe "$SCHEDULER_JOB_NAME" --location="$REGION" &>/dev/null; then
    warn "既存のスケジューラジョブを削除して再作成します..."
    gcloud scheduler jobs delete "$SCHEDULER_JOB_NAME" \
        --location="$REGION" \
        --quiet
fi

# スケジューラジョブを作成
gcloud scheduler jobs create http "$SCHEDULER_JOB_NAME" \
    --location="$REGION" \
    --schedule="$SCHEDULE" \
    --time-zone="$TIMEZONE" \
    --uri="$FUNCTION_URL" \
    --http-method=GET \
    --oidc-service-account-email="$SERVICE_ACCOUNT" \
    --attempt-deadline="600s" \
    --description="動画営業自動化: 週次フロー実行トリガー" \
    --quiet

success "Cloud Scheduler 設定完了"
info "スケジュール: $SCHEDULE ($TIMEZONE)"

# =====================================================
# Step 5: 動作確認
# =====================================================

info "デプロイした関数の動作確認中（dry-run）..."

# Cloud Functions を即座に実行して確認
if gcloud scheduler jobs run "$SCHEDULER_JOB_NAME" \
    --location="$REGION" &>/dev/null; then
    success "スケジューラーからのトリガーテスト成功"
else
    warn "スケジューラーからのトリガーテストをスキップ"
fi

# =====================================================
# 完了メッセージ
# =====================================================

echo ""
echo "========================================"
success "デプロイ完了！"
echo "========================================"
echo ""
echo "【デプロイ情報】"
echo "  関数名: $FUNCTION_NAME"
echo "  リージョン: $REGION"
echo "  URL: $FUNCTION_URL"
echo "  スケジュール: $SCHEDULE ($TIMEZONE)"
echo ""
echo "【確認コマンド】"
echo "  ログ確認:"
echo "    gcloud functions logs read $FUNCTION_NAME --region=$REGION --limit=50"
echo ""
echo "  手動実行:"
echo "    gcloud scheduler jobs run $SCHEDULER_JOB_NAME --location=$REGION"
echo ""
echo "  関数の削除（停止する場合）:"
echo "    gcloud functions delete $FUNCTION_NAME --region=$REGION"
echo "    gcloud scheduler jobs delete $SCHEDULER_JOB_NAME --location=$REGION"
echo ""
echo "【コスト目安】"
echo "  Cloud Functions: 週1回実行で月数十円程度（無料枠内の可能性あり）"
echo "  Cloud Scheduler: 1ジョブ/月 = 無料枠内"
echo "========================================"
