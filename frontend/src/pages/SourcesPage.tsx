/**
 * 数据源管理页面
 */
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { clsx } from "clsx";
import { RefreshCw, ExternalLink, Activity } from "lucide-react";
import { fetchSources, fetchSourcesStatus, triggerCrawl } from "@/services/api";

export function SourcesPage() {
  const queryClient = useQueryClient();

  const { data: sources = [] } = useQuery({
    queryKey: ["sources"],
    queryFn: fetchSources,
  });

  const { data: status } = useQuery({
    queryKey: ["sources-status"],
    queryFn: fetchSourcesStatus,
    refetchInterval: 30 * 1000,
  });

  const crawlMutation = useMutation({
    mutationFn: triggerCrawl,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["sources-status"] });
    },
  });

  const categoryLabels: Record<string, string> = {
    finance: "财经",
    tech: "科技",
    general: "综合",
    world: "国际",
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="text-xl font-bold">数据源管理</h1>
        <p className="text-xs text-gray-400 mt-0.5">
          {status?.total_sources || 0} 个源 ·{" "}
          {status?.total_items || 0} 条新闻
        </p>
      </div>

      {/* 总览卡片 */}
      {status && (
        <div className="grid grid-cols-3 gap-3 mb-6">
          <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50">
            <div className="text-xs text-gray-400 mb-1">总源数</div>
            <div className="text-2xl font-bold font-mono">
              {status.total_sources}
            </div>
          </div>
          <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50">
            <div className="text-xs text-gray-400 mb-1">活跃源</div>
            <div className="text-2xl font-bold font-mono text-green-500">
              {status.active_sources}
            </div>
          </div>
          <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50">
            <div className="text-xs text-gray-400 mb-1">总新闻数</div>
            <div className="text-2xl font-bold font-mono text-blue-500">
              {status.total_items.toLocaleString()}
            </div>
          </div>
        </div>
      )}

      {/* 源列表 */}
      <div className="space-y-2">
        {sources.map((source) => {
          const sourceStatus = status?.sources?.find(
            (s) => s.id === source.id,
          );
          return (
            <div
              key={source.id}
              className="flex items-center gap-4 p-4 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50 hover:border-primary-300 dark:hover:border-primary-700 transition-colors"
            >
              {/* 状态指示灯 */}
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse-slow flex-shrink-0" />

              {/* 源信息 */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-sm">{source.name}</span>
                  <span className="text-xs px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-800 text-gray-500">
                    {categoryLabels[source.category] || source.category}
                  </span>
                </div>
                <div className="flex items-center gap-3 mt-1 text-xs text-gray-400">
                  <span>间隔 {source.crawl_interval}s</span>
                  {sourceStatus && (
                    <span>
                      {sourceStatus.total_items?.toLocaleString() || 0} 条
                    </span>
                  )}
                </div>
              </div>

              {/* 操作 */}
              <div className="flex items-center gap-2">
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400"
                >
                  <ExternalLink size={14} />
                </a>
                <button
                  onClick={() => crawlMutation.mutate(source.id)}
                  disabled={crawlMutation.isPending}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs rounded-lg bg-primary-50 dark:bg-primary-950/30 text-primary-600 dark:text-primary-400 hover:bg-primary-100 dark:hover:bg-primary-900/30 transition-colors disabled:opacity-50"
                >
                  <RefreshCw
                    size={12}
                    className={
                      crawlMutation.isPending ? "animate-spin" : ""
                    }
                  />
                  抓取
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
