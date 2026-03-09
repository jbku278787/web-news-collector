/**
 * 栏目页面 - 按类别浏览新闻
 */
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { RefreshCw } from "lucide-react";
import { Timeline } from "@/components/Timeline";
import { fetchTimeline } from "@/services/api";
import { CATEGORIES } from "@/types";

export function CategoryPage() {
  const { category } = useParams<{ category: string }>();
  const categoryInfo = CATEGORIES.find((c) => c.id === category);

  const {
    data: items = [],
    isLoading,
    isFetching,
    refetch,
  } = useQuery({
    queryKey: ["timeline", category],
    queryFn: () =>
      fetchTimeline({
        category,
        hours: 48,
        limit: 200,
      }),
    refetchInterval: 60 * 1000,
  });

  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-bold">
            {categoryInfo?.label || category}
          </h1>
          <p className="text-xs text-gray-400 mt-0.5">
            最近 48 小时 · {items.length} 条快讯
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

      <Timeline items={items} loading={isLoading} />
    </div>
  );
}
