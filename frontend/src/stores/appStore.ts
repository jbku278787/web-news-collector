/**
 * 全局状态管理
 */
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AppState {
  // 当前选中的栏目
  activeCategory: string;
  setActiveCategory: (category: string) => void;

  // 暗色模式
  darkMode: boolean;
  toggleDarkMode: () => void;

  // 侧边栏
  sidebarOpen: boolean;
  toggleSidebar: () => void;

  // 自动刷新
  autoRefresh: boolean;
  toggleAutoRefresh: () => void;
  refreshInterval: number; // 秒
  setRefreshInterval: (interval: number) => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      activeCategory: "all",
      setActiveCategory: (category) => set({ activeCategory: category }),

      darkMode: true,
      toggleDarkMode: () =>
        set((state) => {
          const newVal = !state.darkMode;
          document.documentElement.classList.toggle("dark", newVal);
          return { darkMode: newVal };
        }),

      sidebarOpen: true,
      toggleSidebar: () =>
        set((state) => ({ sidebarOpen: !state.sidebarOpen })),

      autoRefresh: true,
      toggleAutoRefresh: () =>
        set((state) => ({ autoRefresh: !state.autoRefresh })),
      refreshInterval: 60,
      setRefreshInterval: (interval) => set({ refreshInterval: interval }),
    }),
    {
      name: "newsflow-settings",
    },
  ),
);
