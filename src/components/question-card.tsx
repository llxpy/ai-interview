import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Star, Check, ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"
import type { Question } from "@/data/types"

interface QuestionCardProps {
  question: Question
  index: number
  isDone: boolean
  isStarred: boolean
  onToggleDone: () => void
  onToggleStar: () => void
}

export function QuestionCard({ question, index, isDone, isStarred, onToggleDone, onToggleStar }: QuestionCardProps) {
  const [open, setOpen] = useState(false)

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, delay: Math.min(index * 0.02, 0.3) }}
      className={cn(
        "group bg-card/60 border rounded-xl overflow-hidden transition-all duration-300",
        isDone
          ? "border-success/30 border-l-[3px] border-l-success"
          : "border-border/50 hover:border-primary/25 hover:shadow-[0_0_30px_oklch(0.7_0.14_250/0.08)]"
      )}
    >
      <div className="flex items-start gap-2.5 sm:gap-3 p-3 sm:p-4 cursor-pointer" onClick={() => setOpen(!open)}>
        <div className="min-w-[32px] sm:min-w-[38px] h-8 sm:h-[38px] rounded-lg bg-primary/10 flex items-center justify-center text-xs sm:text-sm font-bold font-mono text-primary shrink-0">
          {question.id}
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-[13px] sm:text-sm leading-relaxed font-medium text-foreground">
            {question.question}
          </div>
          <div className="flex flex-wrap items-center gap-1.5 sm:gap-2 mt-1.5 sm:mt-2">
            <span className="px-2 py-0.5 rounded-md text-[10px] sm:text-[11px] bg-primary/10 text-primary font-medium">
              {question.category}
            </span>
            <div className="flex gap-0.5">
              {Array.from({ length: 4 }, (_, i) => (
                <span key={i} className={cn("text-[10px] sm:text-xs", i < question.difficulty ? "text-warn" : "text-border")}>
                  ★
                </span>
              ))}
            </div>
          </div>
        </div>
        <div className="flex flex-col sm:flex-row items-center gap-0.5 sm:gap-1 shrink-0">
          <button
            onClick={(e) => { e.stopPropagation(); onToggleStar() }}
            className={cn(
              "w-9 h-9 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center transition-all duration-200 active:scale-90",
              isStarred ? "text-warn" : "text-muted-foreground hover:text-foreground"
            )}
          >
            <Star className={cn("w-4 h-4", isStarred && "fill-current")} />
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); onToggleDone() }}
            className={cn(
              "w-9 h-9 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center transition-all duration-200 active:scale-90",
              isDone ? "text-success" : "text-muted-foreground hover:text-foreground"
            )}
          >
            <Check className="w-4 h-4" />
          </button>
          <ChevronDown
            className={cn("w-3.5 h-3.5 text-muted-foreground transition-transform duration-200", open && "rotate-180")}
          />
        </div>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-3 sm:px-4 pb-3 sm:pb-4">
              <div className="bg-background/50 border border-border/30 rounded-xl p-3 sm:p-4">
                <div className="flex items-center gap-2 text-success text-[10px] sm:text-[11px] font-bold uppercase tracking-wider mb-2 sm:mb-3">
                  💡 参考答案
                </div>
                <div className="text-[13px] sm:text-sm leading-relaxed text-muted-foreground whitespace-pre-wrap">
                  {question.answer}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
