import { motion } from "framer-motion"
import { BookOpen } from "lucide-react"


interface HeaderProps {
  total: number
  done: number
  starred: number
  percent: number
}

export function Header({ total, done, starred, percent }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 glass border-b border-border/50">
      <div className="flex items-center justify-between px-4 sm:px-6 h-14 sm:h-16 max-w-[1440px] mx-auto">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-primary to-[oklch(0.7_0.15_290)] flex items-center justify-center glow-border">
            <BookOpen className="w-5 h-5 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-gradient font-display font-bold text-base sm:text-lg leading-tight">
              AI面试宝典
            </h1>
            <p className="text-[10px] sm:text-xs text-muted-foreground leading-tight">
              {total} 道真实面试题
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 sm:gap-5 text-xs sm:text-sm text-muted-foreground">
          <span>
            <span className="text-success mr-1">✓</span>
            <span className="font-mono font-semibold text-success">{done}</span>
          </span>
          <span>
            <span className="text-warn mr-1">★</span>
            <span className="font-mono font-semibold text-warn">{starred}</span>
          </span>
          <span className="hidden xs:inline">
            <span className="font-mono font-semibold text-primary">{percent}%</span>
          </span>
        </div>
      </div>
      <div className="h-0.5 bg-muted">
        <motion.div
          className="h-full bg-gradient-to-r from-primary to-[oklch(0.7_0.15_290)]"
          initial={{ width: 0 }}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
      </div>
    </header>
  )
}
