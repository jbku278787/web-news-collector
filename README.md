# 🗞️ Web News Collector

**开源新闻聚合平台 —— 对标财联社的实时资讯终端**

一个面向财经/科技/综合资讯的全栈新闻聚合系统，支持多源抓取、AI 语义加工、7×24 实时快讯流。

---

## ✨ 核心特性

| 层级 | 能力 | 状态 |
|------|------|------|
| **数据抓取层** | 多源爬虫（财联社、华尔街见闻、东方财富、新浪财经等）+ RSS 通用抓取 | ✅ |
| **内容加工层** | AI 摘要 · 情绪判定（利好/利空/中性）· 行业/板块/个股标签 | ✅ |
| **前端产品层** | 7×24 快讯时间轴 · 栏目切换 · 暗色模式 · 数据源管理 | ✅ |

### 产品形态

- 📰 **快讯时间轴**：财联社风格的 7×24 滚动快讯流
- 🏷️ **智能标签**：AI 自动打标——行业、板块、关联个股
- 📊 **情绪分析**：每条新闻自动判定利好/利空/中性
- 📂 **栏目分类**：财经 / 科技 / 综合 / 国际
- 🌙 **暗色模式**：适合长时间盯盘阅读
- ⚡ **自动刷新**：可配置的定时刷新策略

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────┐
│                   前端 (React)                    │
│  Vite + React 19 + TailwindCSS + TanStack Query  │
│  Zustand 状态管理 · React Router · Lucide Icons   │
└────────────────────┬────────────────────────────┘
                     │ REST API
┌────────────────────▼────────────────────────────┐
│                  后端 (Python)                    │
│         FastAPI + SQLAlchemy + Redis              │
├──────────────┬──────────────┬────────────────────┤
│  API 层      │  爬虫调度器   │  AI 加工引擎        │
│  /api/v1/*   │  APScheduler │  OpenAI / DeepSeek  │
├──────────────┴──────────────┴────────────────────┤
│                  数据存储                          │
│     SQLite (开发) / PostgreSQL (生产) + Redis      │
└──────────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
web-news-collector/
├── backend/                        # Python 后端
│   ├── app/
│   │   ├── api/                    # FastAPI 路由
│   │   │   └── routes/
│   │   │       ├── news.py         # 新闻 CRUD + 过滤
│   │   │       ├── sources.py      # 数据源管理
│   │   │       └── timeline.py     # 7×24 快讯时间轴
│   │   ├── core/                   # 核心配置
│   │   │   ├── config.py           # 环境变量配置
│   │   │   ├── database.py         # 数据库连接
│   │   │   └── cache.py            # Redis 缓存
│   │   ├── crawlers/               # 爬虫系统
│   │   │   ├── base.py             # 爬虫基类
│   │   │   ├── rss_crawler.py      # RSS 通用爬虫
│   │   │   ├── registry.py         # 爬虫注册中心
│   │   │   └── sources/            # 各源爬虫实现
│   │   │       ├── cls.py          # 财联社
│   │   │       ├── wallstreetcn.py # 华尔街见闻
│   │   │       ├── sina_finance.py # 新浪财经
│   │   │       ├── eastmoney.py    # 东方财富
│   │   │       ├── thepaper.py     # 澎湃新闻
│   │   │       └── kr36.py         # 36氪
│   │   ├── processors/             # AI 加工
│   │   │   ├── ai_processor.py     # LLM 语义分析
│   │   │   └── pipeline.py         # 处理管道
│   │   ├── models/                 # 数据模型
│   │   ├── schemas/                # Pydantic Schema
│   │   └── workers/                # 后台任务
│   │       └── crawler_scheduler.py# 定时爬虫调度
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                       # React 前端
│   ├── src/
│   │   ├── components/             # UI 组件
│   │   │   ├── Layout.tsx          # 布局（导航栏+侧边栏）
│   │   │   ├── Timeline.tsx        # 快讯时间轴
│   │   │   ├── NewsCard.tsx        # 新闻卡片
│   │   │   └── StatsBar.tsx        # 统计面板
│   │   ├── pages/                  # 页面
│   │   │   ├── TimelinePage.tsx    # 首页：7×24 快讯
│   │   │   ├── CategoryPage.tsx    # 栏目页
│   │   │   └── SourcesPage.tsx     # 数据源管理
│   │   ├── services/api.ts         # API 客户端
│   │   ├── stores/appStore.ts      # 全局状态
│   │   └── types/index.ts          # 类型定义
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml              # 一键部署
├── Makefile                        # 常用命令
├── .env.example                    # 环境变量模板
└── README.md
```

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 20+ & pnpm
- Redis（可选，无 Redis 时退化为无缓存模式）

### 1. 克隆 & 配置

```bash
git clone https://github.com/your-username/web-news-collector.git
cd web-news-collector

# 复制环境变量
cp .env.example .env
# 编辑 .env，填入你的 LLM API Key（可选）
```

### 2. 安装依赖

```bash
# 一键安装（后端 + 前端）
make install

# 或分别安装
# 后端
cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# 前端
cd frontend && pnpm install
```

### 3. 启动开发服务

```bash
# 同时启动前后端
make dev

# 或分别启动
make dev-backend   # http://localhost:8000
make dev-frontend  # http://localhost:5173
```

### 4. 执行抓取

```bash
# 手动执行一次全量抓取
make crawl

# 或通过 API
curl -X POST http://localhost:8000/api/v1/sources/cls/crawl
```

### 5. Docker 部署

```bash
docker-compose up -d
# 前端: http://localhost:5173
# 后端: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

---

## 📡 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/timeline` | 快讯时间轴（支持栏目过滤、游标分页） |
| GET | `/api/v1/timeline/stats` | 24h 统计（栏目 + 情绪分布） |
| GET | `/api/v1/news` | 新闻列表（源/栏目/情绪/标签/重要性过滤） |
| GET | `/api/v1/news/{id}` | 新闻详情 |
| GET | `/api/v1/news/source/{source_id}` | 按源获取新闻 |
| GET | `/api/v1/sources` | 所有数据源列表 |
| GET | `/api/v1/sources/status` | 源状态概览 |
| POST | `/api/v1/sources/{id}/crawl` | 手动触发抓取 |

完整 API 文档在启动后端后访问：`http://localhost:8000/docs`

---

## 🔌 已接入的新闻源

| 源 | ID | 类型 | 更新频率 |
|----|-----|------|---------|
| 财联社 | `cls` | API | 2 分钟 |
| 华尔街见闻 | `wallstreetcn` | API | 3 分钟 |
| 新浪财经 | `sina_finance` | API | 5 分钟 |
| 东方财富 | `eastmoney` | API | 5 分钟 |
| 澎湃新闻 | `thepaper` | API | 5 分钟 |
| 36氪 | `36kr` | API | 5 分钟 |
| 金色财经 | `jinse` | RSS | 10 分钟 |
| 联合早报 | `zaobao` | RSS | 10 分钟 |
| TechCrunch | `techcrunch` | RSS | 10 分钟 |
| Hacker News | `hackernews` | RSS | 10 分钟 |

### 添加新源

1. 在 `backend/app/crawlers/sources/` 下创建新文件
2. 继承 `BaseCrawler`，实现 `fetch()` 方法
3. 在 `registry.py` 中注册

```python
# backend/app/crawlers/sources/my_source.py
from app.crawlers.base import BaseCrawler
from app.schemas.news import NewsItemCreate

class MySourceCrawler(BaseCrawler):
    source_id = "my_source"
    source_name = "我的新闻源"
    source_url = "https://example.com"
    category = "finance"

    async def fetch(self) -> list[NewsItemCreate]:
        client = await self.get_client()
        # ... 抓取逻辑
        return items
```

---

## 🧠 AI 加工能力

配置 `LLM_API_KEY` 后，每条新闻会自动经过 AI 加工：

- **摘要**：2-3 句话概括核心信息
- **情绪判定**：利好 (positive) / 利空 (negative) / 中性 (neutral)
- **情绪强度**：-1.0 ~ 1.0 量化评分
- **智能标签**：关键词标签、行业板块、关联个股
- **重要性**：0-5 分，5 分为重大事件（央行降息、重大政策等）

支持 OpenAI / DeepSeek / Ollama 等任何兼容 OpenAI API 的 LLM。

---

## 🗺️ 路线图

- [x] v0.1 - 基础架构 & 核心爬虫
- [ ] v0.2 - 用户系统（GitHub OAuth 登录 + 偏好同步）
- [ ] v0.3 - 推送通知（WebSocket 实时推送 + 邮件/微信订阅）
- [ ] v0.4 - 搜索引擎（Elasticsearch 全文检索）
- [ ] v0.5 - 数据看板（行业热度、舆情趋势图表）
- [ ] v0.6 - MCP Server（接入 AI Agent 生态）
- [ ] v0.7 - 移动端适配 & PWA
- [ ] v1.0 - 生产就绪版本

---

## 📄 License

MIT
