/**
 * 统计面板组件
 */
import { TrendingUp, TrendingDown, Activity, BarChart3 } from "lucide-react";

interface StatsBarProps {
  stats?: {
    period: string;
    total: number;
    by_category: Record<string, number>;
    by_sentiment: Record<string, number>;
  };
}

export function StatsBar({ stats }: StatsBarProps) {
  if (!stats) return null;

  const positive = stats.by_sentiment?.positive || 0;
  const negative = stats.by_sentiment?.negative || 0;
  const neutral = stats.by_sentiment?.neutral || 0;

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
      <StatCard
        icon={<Activity size={16} />}
        label="24h 快讯"
        value={stats.total}
        color="blue"
      />
      <StatCard
        icon={<TrendingUp size={16} />}
        label="利好"
        value={positive}
        color="red"
      />
      <StatCard
        icon={<TrendingDown size={16} />}
        label="利空"
        value={negative}
        color="green"
      />
      <StatCard
        icon={<BarChart3 size={16} />}
        label="中性"
        value={neutral}
        color="gray"
      />
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: number;
  color: string;
}) {
  const colorMap: Record<string, string> = {
    blue: "text-blue-500 bg-blue-50 dark:bg-blue-950/30",
    red: "text-red-500 bg-red-50 dark:bg-red-950/30",
    green: "text-green-500 bg-green-50 dark:bg-green-950/30",
    gray: "text-gray-500 bg-gray-50 dark:bg-gray-900",
  };

  return (
    <div className="p-3 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50">
      <div className="flex items-center gap-2 mb-1">
        <div className={`p-1 rounded ${colorMap[color]}`}>{icon}</div>
        <span className="text-xs text-gray-400">{label}</span>
      </div>
      <div className="text-xl font-bold font-mono">{value}</div>
    </div>
  );
}
