import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Star, Check, ChevronDown, Copy, CheckCheck } from "lucide-react"
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
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(question.answer)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, delay: Math.min(index * 0.015, 0.25), ease: "easeOut" }}
      className={cn(
        "group bg-card border rounded-xl overflow-hidden card-hover",
        isDone
          ? "border-success/25 border-l-[3px] border-l-success"
          : "border-border/40"
      )}
    >
      {/* Header */}
      <div
        className="flex items-start gap-3 p-3.5 sm:p-4 cursor-pointer select-none"
        onClick={() => setOpen(!open)}
      >
        <div className={cn(
          "min-w-[30px] sm:min-w-[34px] h-7 sm:h-8 rounded-lg flex items-center justify-center text-[11px] sm:text-xs font-bold font-mono shrink-0 transition-colors",
          isDone ? "bg-success/15 text-success" : "bg-primary/10 text-primary"
        )}>
          {question.id}
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-[13px] sm:text-[14px] leading-[1.65] font-medium text-foreground">
            {question.question}
          </div>
          <div className="flex flex-wrap items-center gap-2 mt-2">
            <span className="px-2 py-0.5 rounded-md text-[10px] sm:text-[11px] bg-primary/8 text-primary/80 font-medium">
              {question.category}
            </span>
            <div className="flex gap-px">
              {Array.from({ length: 4 }, (_, i) => (
                <span key={i} className={cn("text-[10px] sm:text-[11px]", i < question.difficulty ? "text-warn" : "text-border/60")}>
                  ★
                </span>
              ))}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-0.5 sm:gap-1 shrink-0 -mr-1">
          <button
            onClick={(e) => { e.stopPropagation(); onToggleStar() }}
            className={cn(
              "w-8 h-8 sm:w-7 sm:h-7 rounded-md flex items-center justify-center transition-all duration-150 active:scale-90",
              isStarred ? "text-warn" : "text-muted-foreground/50 hover:text-muted-foreground"
            )}
          >
            <Star className={cn("w-3.5 h-3.5 sm:w-3.5 sm:h-3.5", isStarred && "fill-current")} />
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); onToggleDone() }}
            className={cn(
              "w-8 h-8 sm:w-7 sm:h-7 rounded-md flex items-center justify-center transition-all duration-150 active:scale-90",
              isDone ? "text-success" : "text-muted-foreground/50 hover:text-muted-foreground"
            )}
          >
            <Check className="w-3.5 h-3.5 sm:w-3.5 sm:h-3.5" />
          </button>
          <ChevronDown
            className={cn(
              "w-3 h-3 text-muted-foreground/40 transition-transform duration-200 ml-0.5",
              open && "rotate-180 text-primary/60"
            )}
          />
        </div>
      </div>

      {/* Answer */}
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <div className="px-3.5 sm:px-4 pb-3.5 sm:pb-4">
              <div className="answer-container p-3.5 sm:p-4 relative group/answer">
                <div className="flex items-center justify-between mb-2.5">
                  <div className="flex items-center gap-1.5 text-success/80 text-[10px] sm:text-[11px] font-bold uppercase tracking-wider">
                    <span className="w-1 h-1 rounded-full bg-success/60" />
                    参考答案
                  </div>
                  <button
                    onClick={handleCopy}
                    className="opacity-0 group-hover/answer:opacity-100 transition-opacity text-muted-foreground/50 hover:text-muted-foreground p-1 rounded"
                    title="复制答案"
                  >
                    {copied ? <CheckCheck className="w-3.5 h-3.5 text-success" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                </div>
                <div className="text-[13px] sm:text-[13.5px] leading-[1.9] whitespace-pre-wrap">
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
