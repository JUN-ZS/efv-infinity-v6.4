#!/usr/bin/env bash
# ==============================================================================
# EFV∞《永不退電的一朵花》V6.4 — 一鍵建立並推送到 GitHub 新 Repo 腳本
# 用法：
#   方式 A (已安裝 GitHub CLI `gh`)：
#     bash scripts/push_to_github.sh <你的新Repo名稱> [public|private]
#   方式 B (直接指定遠端 GitHub URL)：
#     bash scripts/push_to_github.sh https://github.com/<你的帳號>/<你的新Repo>.git
# ==============================================================================
set -e

ARG1="${1:-efv-infinity-v6.4}"
VISIBILITY="${2:-public}"

echo "🌸 準備推送 EFV∞《永不退電的一朵花》V6.4 Repository..."

# 確保當前為 git repo 且所有變更已提交
if [ ! -d ".git" ]; then
  git init -b main
fi
git add -A
git diff --cached --quiet || git commit -m "chore: update EFV Infinity V6.4 full spec & prompt pipeline"

if [[ "$ARG1" == http* ]] || [[ "$ARG1" == git@* ]]; then
  echo "🔗 設定遠端儲存庫 URL: $ARG1"
  git remote remove origin 2>/dev/null || true
  git remote add origin "$ARG1"
  git branch -M main
  git push -u origin main
  echo "✅ 成功推送到 $ARG1 !"
elif command -v gh >/dev/null 2>&1; then
  echo "🚀 偵測到 GitHub CLI (gh)，正在自動建立新 Repo: $ARG1 ($VISIBILITY)..."
  gh repo create "$ARG1" --"$VISIBILITY" --source=. --remote=origin --push
  echo "✅ 成功建立並推送至 GitHub 新 Repo: $ARG1 !"
else
  echo "⚠️ 未偵測到 GitHub CLI (gh)，請先在 GitHub 網頁建立空 Repo，再執行："
  echo "   git remote add origin https://github.com/<你的GitHub帳號>/$ARG1.git"
  echo "   git branch -M main && git push -u origin main"
fi
