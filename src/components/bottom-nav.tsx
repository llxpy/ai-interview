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
    { icon: LayoutList, label: "全部", active: mode === "list" && !showStarred && !showDoneOnly, color: "text-primary", onClick: onAll },
    { icon: Star, label: "收藏", active: mode === "list" && showStarred, color: "text-warn", onClick: onStarred },
    { icon: Target, label: "刷题", active: mode === "quiz", color: "text-[oklch(0.7_0.15_290)]", onClick: onQuiz },
    { icon: CheckCircle, label: "已掌握", active: mode === "list" && showDoneOnly, color: "text-success", onClick: onDone },
  ]

  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-50 glass border-t border-border/50" style={{ paddingBottom: "env(safe-area-inset-bottom)" }}>
      <div className="flex items-center justify-around h-14">
        {items.map((item) => (
          <button
            key={item.label}
            onClick={item.onClick}
            className={cn(
              "flex flex-col items-center gap-0.5 px-3 py-1 rounded-xl transition-all",
              item.active ? item.color : "text-muted-foreground"
            )}
          >
            <item.icon className="w-5 h-5" />
            <span className="text-[10px]">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  )
}
