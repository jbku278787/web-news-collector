/**
 * 应用布局 - 顶栏 + 侧边栏 + 内容区
 */
import { Outlet, Link, useLocation } from "react-router-dom";
import {
  Newspaper,
  TrendingUp,
  Cpu,
  Globe,
  LayoutGrid,
  Database,
  Sun,
  Moon,
  Menu,
} from "lucide-react";
import { clsx } from "clsx";
import { useAppStore } from "@/stores/appStore";
import { CATEGORIES } from "@/types";

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  all: <LayoutGrid size={18} />,
  finance: <TrendingUp size={18} />,
  tech: <Cpu size={18} />,
  general: <Newspaper size={18} />,
  world: <Globe size={18} />,
};

export function Layout() {
  const location = useLocation();
  const { darkMode, toggleDarkMode, sidebarOpen, toggleSidebar } =
    useAppStore();

  return (
    <div className="min-h-screen flex flex-col">
      {/* 顶部导航栏 */}
      <header className="sticky top-0 z-50 h-14 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-950/80 backdrop-blur-md">
        <div className="h-full flex items-center justify-between px-4">
          {/* 左侧 */}
          <div className="flex items-center gap-3">
            <button
              onClick={toggleSidebar}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 lg:hidden"
            >
              <Menu size={20} />
            </button>
            <Link to="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-primary-500 flex items-center justify-center">
                <Newspaper size={18} className="text-white" />
              </div>
              <span className="text-lg font-bold tracking-tight">
                NewsFlow
              </span>
            </Link>
            <span className="hidden sm:inline text-xs text-gray-400 border-l border-gray-300 dark:border-gray-700 pl-3 ml-1">
              实时资讯终端
            </span>
          </div>

          {/* 右侧工具栏 */}
          <div className="flex items-center gap-2">
            <Link
              to="/sources"
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500"
              title="数据源管理"
            >
              <Database size={18} />
            </Link>
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500"
              title="切换主题"
            >
              {darkMode ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        {/* 侧边栏 - 栏目导航 */}
        <aside
          className={clsx(
            "w-56 border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950",
            "fixed lg:sticky top-14 h-[calc(100vh-3.5rem)] z-40",
            "transition-transform duration-200",
            sidebarOpen
              ? "translate-x-0"
              : "-translate-x-full lg:translate-x-0",
          )}
        >
          <nav className="p-3 space-y-1">
            <div className="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
              栏目
            </div>
            {CATEGORIES.map((cat) => {
              const isActive =
                cat.id === "all"
                  ? location.pathname === "/"
                  : location.pathname === `/category/${cat.id}`;
              return (
                <Link
                  key={cat.id}
                  to={cat.id === "all" ? "/" : `/category/${cat.id}`}
                  className={clsx("category-tab flex items-center gap-3 w-full", {
                    "category-tab--active": isActive,
                  })}
                >
                  {CATEGORY_ICONS[cat.id]}
                  <span>{cat.label}</span>
                </Link>
              );
            })}

            <div className="my-4 border-t border-gray-200 dark:border-gray-800" />
            <div className="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
              工具
            </div>
            <Link
              to="/sources"
              className={clsx("category-tab flex items-center gap-3 w-full", {
                "category-tab--active": location.pathname === "/sources",
              })}
            >
              <Database size={18} />
              <span>数据源</span>
            </Link>
          </nav>
        </aside>

        {/* 主内容区 */}
        <main className="flex-1 min-w-0">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
