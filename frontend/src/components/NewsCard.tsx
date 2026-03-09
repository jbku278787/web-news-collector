/**
 * 新闻卡片组件
 */
import { clsx } from "clsx";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import "dayjs/locale/zh-cn";
import { ExternalLink } from "lucide-react";
import type { NewsItem } from "@/types";

dayjs.extend(relativeTime);
dayjs.locale("zh-cn");

interface NewsCardProps {
  item: NewsItem;
  compact?: boolean;
}

export function NewsCard({ item, compact = false }: NewsCardProps) {
  const time = item.published_at ? dayjs(item.published_at) : null;

  return (
    <article className="news-card group">
      <div className="flex gap-4">
        {/* 封面图 */}
        {!compact && item.cover_image && (
          <div className="flex-shrink-0 w-24 h-16 rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-800">
            <img
              src={item.cover_image}
              alt=""
              className="w-full h-full object-cover"
              loading="lazy"
              onError={(e) => {
                (e.target as HTMLImageElement).style.display = "none";
              }}
            />
          </div>
        )}

        {/* 内容 */}
        <div className="flex-1 min-w-0">
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-medium leading-snug hover:text-primary-500 transition-colors line-clamp-2"
          >
            {item.title}
          </a>

          {/* 摘要 */}
          {!compact && item.summary && (
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400 line-clamp-2">
              {item.summary}
            </p>
          )}

          {/* 底部元信息 */}
          <div className="flex items-center gap-2 mt-2 text-xs text-gray-400">
            {item.author && <span>{item.author}</span>}
            {time && <span>{time.fromNow()}</span>}
            {item.sentiment && item.sentiment !== "neutral" && (
              <span
                className={clsx(
                  "px-1.5 py-0.5 rounded-full text-xs",
                  item.sentiment === "positive"
                    ? "bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400"
                    : "bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400",
                )}
              >
                {item.sentiment === "positive" ? "利好" : "利空"}
              </span>
            )}
            {item.tags?.slice(0, 2).map((tag) => (
              <span
                key={tag}
                className="px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-800"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>

        {/* 外链图标 */}
        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity self-center"
        >
          <ExternalLink size={14} className="text-gray-400" />
        </a>
      </div>
    </article>
  );
}
