import { motion } from "framer-motion"
import { BookOpen, Sun, Moon, Star, CheckCircle, BarChart3 } from "lucide-react"
import { cn } from "@/lib/utils"

interface HeaderProps {
  total: number
  done: number
  starred: number
  percent: number
  theme: "dark" | "light"
  onToggleTheme: () => void
}

export function Header({ total, done, starred, percent, theme, onToggleTheme }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 glass border-b border-border/40">
      <div className="flex items-center justify-between px-4 sm:px-6 h-14 sm:h-16 max-w-[1440px] mx-auto">
        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-gradient-to-br from-primary to-[#a78bfa] flex items-center justify-center shadow-[0_0_12px_color-mix(in_oklab,var(--primary)_25%,transparent)]">
            <BookOpen className="w-4 h-4 sm:w-4.5 sm:h-4.5 text-white" />
          </div>
          <div>
            <h1 className="text-gradient font-display font-bold text-[15px] sm:text-[17px] leading-tight tracking-tight">
              AI面试宝典
            </h1>
            <p className="text-[9px] sm:text-[10px] text-muted-foreground/70 leading-tight font-medium tracking-wide">
              {total.toLocaleString()} 道真实面试题
            </p>
          </div>
        </div>

        {/* Stats */}
        <div className="flex items-center gap-1.5 sm:gap-3">
          <Stat icon={<CheckCircle className="w-3 h-3" />} value={done} color="text-success" className="hidden sm:flex" />
          <Stat icon={<Star className="w-3 h-3" />} value={starred} color="text-warn" className="hidden sm:flex" />
          <Stat icon={<BarChart3 className="w-3 h-3" />} value={`${percent}%`} color="text-primary" className="hidden md:flex" />

          {/* Compact stats for mobile */}
          <div className="flex sm:hidden items-center gap-2.5 text-[11px] text-muted-foreground">
            <span className="font-mono text-success">{done}</span>
            <span className="text-border">|</span>
            <span className="font-mono text-warn">{starred}</span>
          </div>

          {/* Theme toggle */}
          <button
            onClick={onToggleTheme}
            className={cn(
              "w-8 h-8 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center transition-all duration-200",
              "text-muted-foreground/60 hover:text-foreground hover:bg-accent active:scale-95"
            )}
            title={theme === "dark" ? "切换亮色" : "切换暗色"}
          >
            <motion.div
              key={theme}
              initial={{ rotate: -30, opacity: 0, scale: 0.8 }}
              animate={{ rotate: 0, opacity: 1, scale: 1 }}
              transition={{ duration: 0.2 }}
            >
              {theme === "dark" ? <Sun className="w-[17px] h-[17px]" /> : <Moon className="w-[17px] h-[17px]" />}
            </motion.div>
          </button>
        </div>
      </div>

      {/* Progress bar */}
      <div className="h-[2px] bg-muted/50">
        <motion.div
          className="h-full bg-gradient-to-r from-primary via-[#a78bfa] to-[#67e8f9]"
          initial={{ width: 0 }}
          animate={{ width: `${Math.max(percent, 0.5)}%` }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        />
      </div>
    </header>
  )
}

function Stat({ icon, value, color, className }: { icon: React.ReactNode; value: string | number; color: string; className?: string }) {
  return (
    <div className={cn("flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-secondary/50 text-xs", className)}>
      <span className={color}>{icon}</span>
      <span className={cn("font-mono font-semibold text-[12px]", color)}>{value}</span>
    </div>
  )
}
