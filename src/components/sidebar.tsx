import { cn } from "@/lib/utils"
import type { CategoryInfo } from "@/data/types"
import { Shuffle, RotateCcw } from "lucide-react"

interface SidebarProps {
  categories: CategoryInfo[]
  current: string
  onSelect: (name: string) => void
  doneCount: number
  totalCount: number
  percent: number
  onRandomQuiz: () => void
  onReset: () => void
}

export function Sidebar({ categories, current, onSelect, doneCount, totalCount, percent, onRandomQuiz, onReset }: SidebarProps) {
  return (
    <aside className="hidden lg:flex flex-col w-60 min-w-[240px] border-r border-border/50 bg-grid overflow-y-auto sticky top-14 h-[calc(100vh-3.5rem)]">
      <div className="p-4">
        <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-medium mb-3 px-2">题目分类</p>
        <div className="space-y-0.5">
          {categories.map((cat) => (
            <button
              key={cat.name}
              onClick={() => onSelect(cat.name)}
              className={cn(
                "flex items-center justify-between w-full px-3 py-2 rounded-xl cursor-pointer transition-all duration-200 text-sm text-left",
                current === cat.name
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground"
              )}
            >
              <span className="flex items-center gap-2">
                <span className="text-base">{cat.icon}</span>
                {cat.name}
              </span>
              <span
                className={cn(
                  "text-[11px] font-mono px-2 py-0.5 rounded-md",
                  current === cat.name ? "bg-primary/15 text-primary" : "bg-card text-muted-foreground"
                )}
              >
                {cat.count}
              </span>
            </button>
          ))}
        </div>

        <div className="mt-6 pt-4 border-t border-border/40">
          <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-medium mb-3 px-2">快捷操作</p>
          <div className="space-y-0.5">
            <button
              onClick={onRandomQuiz}
              className="flex items-center gap-2 w-full px-3 py-2 rounded-xl cursor-pointer text-sm text-muted-foreground hover:bg-accent hover:text-foreground transition-all text-left"
            >
              <Shuffle className="w-4 h-4" /> 随机抽题
            </button>
            <button
              onClick={() => { if (confirm("确定重置所有进度？")) onReset() }}
              className="flex items-center gap-2 w-full px-3 py-2 rounded-xl cursor-pointer text-sm text-destructive/70 hover:bg-destructive/10 hover:text-destructive transition-all text-left"
            >
              <RotateCcw className="w-4 h-4" /> 重置进度
            </button>
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-border/40 px-2">
          <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-medium mb-3">总进度</p>
          <div className="flex justify-between text-xs text-muted-foreground mb-2">
            <span className="font-mono">{doneCount}/{totalCount}</span>
            <span className="font-mono text-primary">{percent}%</span>
          </div>
          <div className="h-1.5 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-primary to-[oklch(0.7_0.15_290)] transition-all duration-500"
              style={{ width: `${percent}%` }}
            />
          </div>
        </div>
      </div>
    </aside>
  )
}
