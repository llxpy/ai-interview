import { LayoutList, Star, Target, CheckCircle } from "lucide-react"
import { cn } from "@/lib/utils"

interface BottomNavProps {
  mode: "list" | "quiz"
  showStarred: boolean
  showDoneOnly: boolean
  onAll: () => void
  onStarred: () => void
  onDone: () => void
  onQuiz: () => void
}

export function BottomNav({ mode, showStarred, showDoneOnly, onAll, onStarred, onDone, onQuiz }: BottomNavProps) {
  const items = [
    { icon: LayoutList, label: "全部", active: mode === "list" && !showStarred && !showDoneOnly, color: "text-primary", bg: "bg-primary/10", onClick: onAll },
    { icon: Star, label: "收藏", active: mode === "list" && showStarred, color: "text-warn", bg: "bg-warn/10", onClick: onStarred },
    { icon: Target, label: "刷题", active: mode === "quiz", color: "text-[#a78bfa]", bg: "bg-[#a78bfa]/10", onClick: onQuiz },
    { icon: CheckCircle, label: "已掌握", active: mode === "list" && showDoneOnly, color: "text-success", bg: "bg-success/10", onClick: onDone },
  ]

  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-50 glass border-t border-border/30" style={{ paddingBottom: "env(safe-area-inset-bottom)" }}>
      <div className="flex items-center justify-around h-[52px] px-2">
        {items.map((item) => (
          <button
            key={item.label}
            onClick={item.onClick}
            className={cn(
              "flex flex-col items-center gap-0.5 px-4 py-1.5 rounded-xl transition-all duration-200 min-w-[56px]",
              item.active ? cn(item.color, item.bg) : "text-muted-foreground/50 active:text-muted-foreground"
            )}
          >
            <item.icon className={cn("w-[18px] h-[18px] transition-transform", item.active && "scale-110")} />
            <span className={cn("text-[9px] font-medium tracking-wide", item.active && "font-semibold")}>{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  )
}
