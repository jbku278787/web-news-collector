/**
 * 核心类型定义
 */

// 新闻条目
export interface NewsItem {
  id: string;
  title: string;
  url: string;
  source_id: string;
  content?: string;
  summary?: string;
  cover_image?: string;
  author?: string;
  sentiment?: "positive" | "negative" | "neutral";
  sentiment_score?: number;
  tags?: string[];
  sectors?: string[];
  stocks?: string[];
  importance: number;
  published_at?: string;
  crawled_at: string;
  processed_at?: string;
  category?: string;
}

// 时间轴条目
export interface TimelineItem {
  id: string;
  title: string;
  url: string;
  source_id: string;
  source_name: string;
  summary?: string;
  sentiment?: "positive" | "negative" | "neutral";
  tags?: string[];
  importance: number;
  published_at?: string;
}

// 新闻源
export interface NewsSource {
  id: string;
  name: string;
  url: string;
  category: string;
  crawl_interval: number;
  favicon?: string;
  color?: string;
}

// 新闻列表响应
export interface NewsListResponse {
  items: NewsItem[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

// 带状态信息的新闻源（包含统计字段）
export interface NewsSourceWithStatus extends NewsSource {
  total_items?: number;
}

// 源状态
export interface SourceStatus {
  total_sources: number;
  active_sources: number;
  total_items: number;
  sources: NewsSourceWithStatus[];
}

// 栏目定义
export interface Category {
  id: string;
  label: string;
  icon: string;
  color: string;
}

export const CATEGORIES: Category[] = [
  { id: "all", label: "全部", icon: "LayoutGrid", color: "blue" },
  { id: "finance", label: "财经", icon: "TrendingUp", color: "red" },
  { id: "tech", label: "科技", icon: "Cpu", color: "purple" },
  { id: "general", label: "综合", icon: "Newspaper", color: "gray" },
  { id: "world", label: "国际", icon: "Globe", color: "green" },
];
