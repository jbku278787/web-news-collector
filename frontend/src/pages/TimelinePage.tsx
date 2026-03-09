/**
 * 时间轴页面 - 7×24 快讯流（首页）
 */
import { useQuery } from "@tanstack/react-query";
import { RefreshCw } from "lucide-react";
import { Timeline } from "@/components/Timeline";
import { StatsBar } from "@/components/StatsBar";
import { fetchTimeline, fetchTimelineStats } from "@/services/api";
import { useAppStore } from "@/stores/appStore";

export function TimelinePage() {
  const { activeCategory, autoRefresh, refreshInterval } = useAppStore();

  const {
    data: items = [],
    isLoading,
    isFetching,
    refetch,
  } = useQuery({
    queryKey: ["timeline", activeCategory],
    queryFn: () =>
      fetchTimeline({
        category: activeCategory === "all" ? undefined : activeCategory,
        hours: 24,
        limit: 200,
      }),
    refetchInterval: autoRefresh ? refreshInterval * 1000 : false,
  });

  const { data: stats } = useQuery({
    queryKey: ["timeline-stats"],
    queryFn: fetchTimelineStats,
    refetchInterval: 5 * 60 * 1000, // 5 分钟刷新统计
  });

  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-bold">7×24 快讯</h1>
          <p className="text-xs text-gray-400 mt-0.5">
            实时资讯 · 多源聚合 · AI 加工
          </p>
        </div>
        <button
          onClick={() => refetch()}
          disabled={isFetching}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-500 hover:text-primary-500 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors disabled:opacity-50"
        >
          <RefreshCw
            size={14}
            className={isFetching ? "animate-spin" : ""}
          />
          刷新
        </button>
      </div>

      {/* 统计面板 */}
      <StatsBar stats={stats} />

      {/* 快讯时间轴 */}
      <Timeline items={items} loading={isLoading} />
    </div>
  );
}
