# 安装 Python 3.11+
python3 -m venv /opt/web-news-collector/backend/.venv
source /opt/web-news-collector/backend/.venv/bin/activate
pip install -r /opt/web-news-collector/backend/requirements.txt

# 用 systemd 管理进程.PHONY: help dev dev-backend dev-frontend install install-backend install-frontend \
       build lint test clean docker-up docker-down crawl

# ---------- 默认 ----------
help: ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ---------- 安装依赖 ----------
install: install-backend install-frontend ## 安装全部依赖

install-backend: ## 安装后端依赖
	cd backend && python -m venv .venv && \
		source .venv/bin/activate && \
		pip install -r requirements.txt

install-frontend: ## 安装前端依赖
	cd frontend && pnpm install

# ---------- 开发模式 ----------
dev: ## 同时启动前后端开发服务
	@make -j2 dev-backend dev-frontend

dev-backend: ## 启动后端开发服务
	cd backend && source .venv/bin/activate && \
		uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## 启动前端开发服务
	cd frontend && pnpm dev

# ---------- 构建 ----------
build: ## 构建前端生产版本
	cd frontend && pnpm build

# ---------- 爬虫 ----------
crawl: ## 手动执行一次全量抓取
	cd backend && source .venv/bin/activate && \
		python -m app.workers.crawler_scheduler --once

# ---------- 测试 ----------
test: ## 运行全部测试
	cd backend && source .venv/bin/activate && pytest -v
	cd frontend && pnpm test

lint: ## 运行代码检查
	cd backend && source .venv/bin/activate && ruff check .
	cd frontend && pnpm lint

# ---------- Docker ----------
docker-up: ## Docker 启动全部服务
	docker-compose up -d --build

docker-down: ## Docker 停止全部服务
	docker-compose down

# ---------- 清理 ----------
clean: ## 清理构建产物和缓存
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf frontend/dist backend/dist
