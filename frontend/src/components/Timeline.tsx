/**
 * 快讯时间轴组件 - 核心展示组件
 * 模拟财联社 7×24 快讯流
 */
import { clsx } from "clsx";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import "dayjs/locale/zh-cn";
import { ExternalLink, ChevronUp } from "lucide-react";
import type { TimelineItem } from "@/types";

dayjs.extend(relativeTime);
dayjs.locale("zh-cn");

interface TimelineProps {
  items: TimelineItem[];
  loading?: boolean;
}

export function Timeline({ items, loading }: TimelineProps) {
  if (loading) {
    return <TimelineSkeleton />;
  }

  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-gray-400">
        <p className="text-lg">暂无快讯</p>
        <p className="text-sm mt-1">等待爬虫抓取新数据...</p>
      </div>
    );
  }

  // 按日期分组
  const grouped = groupByDate(items);

  return (
    <div className="relative pl-6">
      {/* 时间轴竖线 */}
      <div className="timeline-line" />

      {Object.entries(grouped).map(([date, dateItems]) => (
        <div key={date} className="mb-6">
          {/* 日期标题 */}
          <div className="sticky top-14 z-10 -ml-6 mb-3 py-1">
            <span className="inline-block px-3 py-1 text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-950 rounded-full border border-gray-200 dark:border-gray-800">
              {date}
            </span>
          </div>

          {/* 该日期的新闻列表 */}
          <div className="space-y-0">
            {dateItems.map((item) => (
              <TimelineEntry key={item.id} item={item} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function TimelineEntry({ item }: { item: TimelineItem }) {
  const isImportant = item.importance >= 3;
  const time = item.published_at ? dayjs(item.published_at) : null;

  return (
    <div className={clsx("relative py-3 group animate-slide-up", {
      "bg-red-50/50 dark:bg-red-950/10 -mx-4 px-4 rounded-lg": isImportant,
    })}>
      {/* 时间轴圆点 */}
      <div
        className={clsx("timeline-dot", {
          "timeline-dot--important": isImportant,
        })}
      />

      <div className="flex items-start gap-3">
        {/* 时间 */}
        <div className="w-12 flex-shrink-0 text-xs text-gray-400 pt-0.5 font-mono">
          {time ? time.format("HH:mm") : "--:--"}
        </div>

        {/* 内容 */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start gap-2">
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className={clsx(
                "text-sm leading-relaxed hover:text-primary-500 transition-colors",
                isImportant ? "font-semibold text-red-700 dark:text-red-400" : "",
              )}
            >
              {item.title}
            </a>
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0 mt-0.5"
            >
              <ExternalLink size={14} className="text-gray-400" />
            </a>
          </div>

          {/* 元信息行 */}
          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
            {/* 来源 */}
            <span className="text-xs text-gray-400">
              {item.source_name}
            </span>

            {/* 情绪标签 */}
            {item.sentiment && item.sentiment !== "neutral" && (
              <SentimentBadge sentiment={item.sentiment} />
            )}

            {/* 标签 */}
            {item.tags?.slice(0, 3).map((tag) => (
              <span
                key={tag}
                className="text-xs px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400"
              >
                {tag}
              </span>
            ))}

            {/* 相对时间 */}
            <span className="text-xs text-gray-300 dark:text-gray-600 ml-auto">
              {time ? time.fromNow() : ""}
            </span>
          </div>

          {/* 摘要（重要新闻展示） */}
          {isImportant && item.summary && (
            <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 leading-relaxed border-l-2 border-red-300 dark:border-red-700 pl-3">
              {item.summary}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function SentimentBadge({
  sentiment,
}: {
  sentiment: "positive" | "negative" | "neutral";
}) {
  const labels = {
    positive: "利好",
    negative: "利空",
    neutral: "中性",
  };
  return (
    <span className={`sentiment-badge sentiment-badge--${sentiment}`}>
      {sentiment === "positive" && <ChevronUp size={12} className="mr-0.5" />}
      {labels[sentiment]}
    </span>
  );
}

function TimelineSkeleton() {
  return (
    <div className="relative pl-6 space-y-4">
      <div className="timeline-line" />
      {[...Array(8)].map((_, i) => (
        <div key={i} className="relative py-3 animate-pulse">
          <div className="timeline-dot bg-gray-300 dark:bg-gray-700" />
          <div className="flex items-start gap-3">
            <div className="w-12 h-4 bg-gray-200 dark:bg-gray-800 rounded" />
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-gray-200 dark:bg-gray-800 rounded w-3/4" />
              <div className="h-3 bg-gray-200 dark:bg-gray-800 rounded w-1/2" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

// ---- 工具函数 ----

function groupByDate(items: TimelineItem[]): Record<string, TimelineItem[]> {
  const groups: Record<string, TimelineItem[]> = {};
  for (const item of items) {
    const date = item.published_at
      ? dayjs(item.published_at).format("MM月DD日 dddd")
      : "未知日期";
    if (!groups[date]) groups[date] = [];
    groups[date].push(item);
  }
  return groups;
}
