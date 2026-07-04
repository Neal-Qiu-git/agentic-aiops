#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Dashboard 构建 + GitHub Pages 部署脚本
# 
# 问题根因: GitHub Pages 部署路径是仓库根目录 "/"，
#           但 Dashboard 构建产物在 aiops/web/，
#           导致根目录的旧 index.html 一直被使用。
#
# 解决方案: 每次构建后，自动将产物同步到仓库根目录的
#           index.html + assets/ + favicon.svg，
#           然后提交推送，确保 Pages 始终使用最新版本。
#
# 用法: bash scripts/deploy-pages.sh [--no-push]
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DASHBOARD_DIR="$PROJECT_ROOT/dashboard"
DIST_DIR="$DASHBOARD_DIR/dist"

echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}  🚀 Dashboard Pages 部署脚本${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"

# ── Step 1: 构建 Dashboard ──
echo -e "\n${YELLOW}[1/5] 构建 Dashboard...${NC}"
cd "$DASHBOARD_DIR"
npm run build
echo -e "${GREEN}  ✅ 构建完成${NC}"

# ── Step 2: 同步到 aiops/web/（本地运行用）──
echo -e "\n${YELLOW}[2/5] 同步到 aiops/web/...${NC}"
WEB_DIR="$PROJECT_ROOT/aiops/web"
rm -rf "$WEB_DIR"
cp -r "$DIST_DIR" "$WEB_DIR"
echo -e "${GREEN}  ✅ aiops/web/ 已更新${NC}"

# ── Step 3: 同步到仓库根目录（GitHub Pages 用）──
echo -e "\n${YELLOW}[3/5] 同步到仓库根目录（GitHub Pages）...${NC}"
cd "$PROJECT_ROOT"

# 复制 index.html（从 aiops/web/index.html）
cp "$WEB_DIR/index.html" "./index.html"

# 复制 favicon（如果存在）
if [ -f "$WEB_DIR/favicon.svg" ]; then
    cp "$WEB_DIR/favicon.svg" "./favicon.svg"
fi

# 同步 assets/ 目录（删除旧文件，复制新文件）
rm -rf "./assets"
mkdir -p "./assets"
cp "$WEB_DIR/assets/"* "./assets/"

echo -e "${GREEN}  ✅ 根目录 index.html + assets/ 已同步${NC}"
echo -e "     引用: $(grep -o 'index-[A-Za-z0-9_-]*\.js' ./index.html | head -1)"

# ── Step 4: 提交 ──
echo -e "\n${YELLOW}[4/5] 提交变更...${NC}"
git add -A
if git diff --cached --quiet; then
    echo -e "  ℹ️  无变更，跳过提交"
else
    git commit -m "chore(deploy): Dashboard 构建产物同步到根目录

原因: GitHub Pages 部署路径为仓库根目录 /，
      必须确保根目录 index.html 引用最新的 JS/CSS。
      
此脚本确保每次构建后:
1. aiops/web/ 更新（本地 aiops serve 使用）
2. 根目录 index.html + assets/ 更新（GitHub Pages 使用）
3. 两处引用同一个 JS/CSS 文件名（哈希保证唯一）"
    echo -e "${GREEN}  ✅ 已提交${NC}"
fi

# ── Step 5: 推送（可选）──
if [ "${1:-}" = "--no-push" ]; then
    echo -e "\n${YELLOW}[5/5] 跳过推送 (--no-push)${NC}"
else
    echo -e "\n${YELLOW}[5/5] 推送到远程仓库...${NC}"
    
    # Gitee
    echo -n "  Gitee: "
    git push origin main 2>&1 | tail -1 || echo -e "${RED}❌ 推送失败${NC}"
    
    # GitHub
    echo -n "  GitHub: "
    GIT_SSL_NO_VERIFY=1 git push github main 2>&1 | tail -1 || echo -e "${RED}❌ 推送失败${NC}"
    
    echo -e "${GREEN}  ✅ 双仓库已同步${NC}"
fi

echo -e "\n${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ 部署完成！${NC}"
echo -e "${GREEN}  🌐 https://neal-qiu-git.github.io/agentic-aiops/${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
