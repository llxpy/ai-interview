import { cn } from "@/lib/utils"
import type { CategoryInfo } from "@/data/types"
import { Shuffle, RotateCcw } from "lucide-react"

interface CategoryDrawerProps {
  open: boolean
  onClose: () => void
  categories: CategoryInfo[]
  current: string
  onSelect: (name: string) => void
  onRandomQuiz: () => void
  onReset: () => void
}

export function CategoryDrawer({ open, onClose, categories, current, onSelect, onRandomQuiz, onReset }: CategoryDrawerProps) {
  if (!open) return null

  return (
    <>
      <div className="fixed inset-0 z-60 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div
        className={cn(
          "fixed left-0 right-0 bottom-0 z-70 max-h-[75vh] overflow-y-auto",
          "bg-card border-t border-border rounded-t-2xl",
          "transition-transform duration-250",
          open ? "translate-y-0" : "translate-y-full"
        )}
      >
        <div className="w-9 h-1 bg-border rounded-full mx-auto mt-2.5" />
        <div className="p-4 pb-8">
          <p className="text-xs text-muted-foreground uppercase tracking-widest font-medium mb-3 px-2">选择分类</p>
          <div className="grid grid-cols-2 gap-2">
            {categories.map((cat) => (
              <button
                key={cat.name}
                onClick={() => { onSelect(cat.name); onClose() }}
                className={cn(
                  "flex items-center gap-2 px-3 py-3 rounded-xl cursor-pointer transition-all text-sm border text-left",
                  current === cat.name
                    ? "bg-primary/10 border-primary/30 text-primary"
                    : "bg-card border-border/30 text-muted-foreground active:bg-accent"
                )}
              >
                <span>{cat.icon}</span>
                <span className="flex-1 truncate">{cat.name}</span>
                <span className="text-[10px] font-mono opacity-60">{cat.count}</span>
              </button>
            ))}
          </div>
          <div className="mt-4 pt-3 border-t border-border/30 grid grid-cols-2 gap-2">
            <button
              onClick={() => { onRandomQuiz(); onClose() }}
              className="flex items-center justify-center gap-2 px-3 py-3 rounded-xl border border-border/30 bg-card text-muted-foreground text-sm active:bg-accent transition-all"
            >
              <Shuffle className="w-4 h-4" /> 随机抽题
            </button>
            <button
              onClick={() => { if (confirm("确定重置所有进度？")) { onReset(); onClose() } }}
              className="flex items-center justify-center gap-2 px-3 py-3 rounded-xl border border-destructive/20 bg-card text-destructive/60 text-sm active:bg-destructive/10 transition-all"
            >
              <RotateCcw className="w-4 h-4" /> 重置进度
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
