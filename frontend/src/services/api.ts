/**
 * API 客户端
 */
import type {
  NewsItem,
  NewsListResponse,
  NewsSource,
  SourceStatus,
  TimelineItem,
} from "@/types";

const API_BASE = "/api/v1";

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

// ---- 时间轴 ----

export function fetchTimeline(params?: {
  category?: string;
  hours?: number;
  limit?: number;
  before?: string;
}): Promise<TimelineItem[]> {
  const searchParams = new URLSearchParams();
  if (params?.category && params.category !== "all") {
    searchParams.set("category", params.category);
  }
  if (params?.hours) searchParams.set("hours", String(params.hours));
  if (params?.limit) searchParams.set("limit", String(params.limit));
  if (params?.before) searchParams.set("before", params.before);
  const qs = searchParams.toString();
  return fetchJSON(`/timeline${qs ? `?${qs}` : ""}`);
}

export function fetchTimelineStats(): Promise<{
  period: string;
  total: number;
  by_category: Record<string, number>;
  by_sentiment: Record<string, number>;
}> {
  return fetchJSON("/timeline/stats");
}

// ---- 新闻 ----

export function fetchNews(params?: {
  source_id?: string;
  category?: string;
  sentiment?: string;
  page?: number;
  page_size?: number;
}): Promise<NewsListResponse> {
  const searchParams = new URLSearchParams();
  if (params?.source_id) searchParams.set("source_id", params.source_id);
  if (params?.category) searchParams.set("category", params.category);
  if (params?.sentiment) searchParams.set("sentiment", params.sentiment);
  if (params?.page) searchParams.set("page", String(params.page));
  if (params?.page_size)
    searchParams.set("page_size", String(params.page_size));
  const qs = searchParams.toString();
  return fetchJSON(`/news${qs ? `?${qs}` : ""}`);
}

export function fetchNewsDetail(id: string): Promise<NewsItem> {
  return fetchJSON(`/news/${id}`);
}

// ---- 源 ----

export function fetchSources(): Promise<NewsSource[]> {
  return fetchJSON("/sources");
}

export function fetchSourcesStatus(): Promise<SourceStatus> {
  return fetchJSON("/sources/status");
}

export function triggerCrawl(
  sourceId: string,
): Promise<{ message: string; source: string }> {
  return fetchJSON(`/sources/${sourceId}/crawl`, { method: "POST" });
}
