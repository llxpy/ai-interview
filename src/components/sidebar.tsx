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
    <aside className="hidden lg:flex flex-col w-[232px] min-w-[232px] border-r border-border/30 overflow-y-auto sticky top-14 h-[calc(100vh-3.5rem)]">
      <div className="p-3">
        <p className="text-[9px] text-muted-foreground/50 uppercase tracking-[0.12em] font-semibold mb-2.5 px-2.5">题目分类</p>
        <div className="space-y-px">
          {categories.map((cat) => (
            <button
              key={cat.name}
              onClick={() => onSelect(cat.name)}
              className={cn(
                "flex items-center justify-between w-full px-2.5 py-[7px] rounded-lg cursor-pointer transition-all duration-150 text-[13px] text-left group",
                current === cat.name
                  ? "bg-primary/10 text-primary font-medium"
                  : "text-muted-foreground hover:bg-accent/60 hover:text-foreground"
              )}
            >
              <span className="flex items-center gap-2">
                <span className="text-[14px]">{cat.icon}</span>
                <span className="truncate">{cat.name}</span>
              </span>
              <span
                className={cn(
                  "text-[10px] font-mono px-1.5 py-px rounded-md transition-colors",
                  current === cat.name ? "bg-primary/15 text-primary" : "bg-transparent text-muted-foreground/40 group-hover:text-muted-foreground/60"
                )}
              >
                {cat.count}
              </span>
            </button>
          ))}
        </div>

        <div className="mt-5 pt-4 border-t border-border/20">
          <p className="text-[9px] text-muted-foreground/50 uppercase tracking-[0.12em] font-semibold mb-2.5 px-2.5">快捷操作</p>
          <div className="space-y-px">
            <button
              onClick={onRandomQuiz}
              className="flex items-center gap-2 w-full px-2.5 py-[7px] rounded-lg cursor-pointer text-[13px] text-muted-foreground hover:bg-accent/60 hover:text-foreground transition-all text-left"
            >
              <Shuffle className="w-3.5 h-3.5" /> 随机抽题
            </button>
            <button
              onClick={() => { if (confirm("确定重置所有进度？")) onReset() }}
              className="flex items-center gap-2 w-full px-2.5 py-[7px] rounded-lg cursor-pointer text-[13px] text-destructive/50 hover:bg-destructive/8 hover:text-destructive transition-all text-left"
            >
              <RotateCcw className="w-3.5 h-3.5" /> 重置进度
            </button>
          </div>
        </div>

        {/* Progress card */}
        <div className="mt-5 pt-4 border-t border-border/20 px-2.5">
          <p className="text-[9px] text-muted-foreground/50 uppercase tracking-[0.12em] font-semibold mb-3">学习进度</p>
          <div className="bg-secondary/40 rounded-xl p-3">
            <div className="flex items-end justify-between mb-2">
              <span className="text-2xl font-display font-bold text-foreground">{percent}<span className="text-sm text-muted-foreground ml-0.5">%</span></span>
              <span className="text-[10px] text-muted-foreground font-mono">{doneCount}/{totalCount}</span>
            </div>
            <div className="h-1.5 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-primary to-[#a78bfa] transition-all duration-700 ease-out"
                style={{ width: `${Math.max(percent, 0.5)}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
