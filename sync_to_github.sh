#!/bin/bash
# GitHub Pages 数据同步脚本
# 用途：将项目空间的数据文件同步推送到 GitHub Pages 仓库
# 使用方式：在日程任务中，先更新coze.cn项目空间的JSON，然后执行此脚本

set -e

REPO_DIR="/tmp/trading-dashboard"
PROJECT_ID="7649040348093661503"

# 确保仓库存在
if [ ! -d "$REPO_DIR/.git" ]; then
    mkdir -p "$REPO_DIR"
    cd "$REPO_DIR"
    git clone https://x-access-token:$(gh auth token)@github.com/bestwisebear/trading-dashboard-v3.git .
fi

cd "$REPO_DIR"
git fetch origin main
git reset --hard origin/main

# 下载项目空间中所有数据文件
FILES=(
    "positions.json"
    "trades_today.json"
    "market_signals.json"
    "watchlist.json"
    "oversold_sectors.json"
    "bottom_signals.json"
    "market_environment.json"
    "plans.json"
    "risk_assessment.json"
    "discipline_log.json"
    "avoid_list.json"
    "reviews_daily.json"
    "reviews_weekly.json"
    "reviews_monthly.json"
    "fundamentals.json"
    "news_impact.json"
    "quick_eval.json"
)

for f in "${FILES[@]}"; do
    coze agent file download --project-id "$PROJECT_ID" --project-file-path "/看板V3/data/$f" 2>/dev/null
    if [ -f "$f" ]; then
        cp "$f" "data/$f"
        echo "✓ Synced $f"
    else
        echo "✗ Skipped $f (not found)"
    fi
done

# 提交并推送
git add data/
if git diff --cached --quiet; then
    echo "No changes to push."
else
    git commit -m "auto sync: $(date '+%Y-%m-%d %H:%M') data update"
    git push origin main
    echo "✓ Pushed to GitHub Pages"
fi
