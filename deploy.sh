#!/bin/bash
# Agentic AIOps 一键部署脚本
# 用法: curl -sL <url>/deploy.sh | bash

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════╗"
echo "║     🤖 Agentic AIOps 一键部署           ║"
echo "║     AI-native Operations Platform        ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "${NC}"

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker 未安装，请先安装 Docker${NC}"
    echo "   curl -fsSL https://get.docker.com | sh"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose 未安装${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker 环境检查通过${NC}"

# 创建项目目录
INSTALL_DIR="${INSTALL_DIR:-/opt/agentic-aiops}"
echo -e "${YELLOW}📁 安装目录: ${INSTALL_DIR}${NC}"

if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}📥 克隆项目...${NC}"
    git clone https://gitee.com/neal4752/agentic-aiops.git "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# 配置环境变量
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚙️  创建配置文件...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  请编辑 ${INSTALL_DIR}/.env 填入 AI API Key${NC}"
    echo -e "${YELLOW}   vim ${INSTALL_DIR}/.env${NC}"
    echo ""
    read -p "是否现在编辑 .env？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-vim} .env
    fi
fi

# 启动服务
echo -e "${GREEN}🚀 启动服务...${NC}"
docker compose up -d

# 健康检查
echo -e "${YELLOW}⏳ 等待服务启动...${NC}"
sleep 5

if curl -sf http://localhost:3001/health > /dev/null 2>&1; then
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════╗"
    echo "║  ✅ 部署成功！                            ║"
    echo "║                                           ║"
    echo "║  🌐 API: http://localhost:3001            ║"
    echo "║  📋 Health: http://localhost:3001/health  ║"
    echo "║  📖 Docs: http://localhost:3001/docs      ║"
    echo "║                                           ║"
    echo "║  默认账号: admin / admin                   ║"
    echo "║  ⚠️  首次登录请修改密码                    ║"
    echo "╚═══════════════════════════════════════════╝"
    echo -e "${NC}"
else
    echo -e "${YELLOW}⏳ 服务启动中，请稍等...${NC}"
    echo -e "${YELLOW}   docker compose logs -f 查看日志${NC}"
fi
