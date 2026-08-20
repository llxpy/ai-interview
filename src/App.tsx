import { useState, useMemo, useCallback, useEffect } from "react"
import { motion } from "framer-motion"
import { Search, Filter, LayoutList, Target, Star, ChevronLeft, ChevronRight } from "lucide-react"
import { cn } from "@/lib/utils"
import { useQuestions } from "@/lib/use-questions"
import { Header } from "@/components/header"
import { Sidebar } from "@/components/sidebar"
import { QuestionCard } from "@/components/question-card"
import { BottomNav } from "@/components/bottom-nav"
import { CategoryDrawer } from "@/components/category-drawer"
import type { Question } from "@/data/types"

const PAGE_SIZE = 20

const DIFF_FILTERS = [
  { v: 0, l: "全" },
  { v: 1, l: "★" },
  { v: 2, l: "★★" },
  { v: 3, l: "★★★" },
  { v: 4, l: "★★★★" },
]

export default function App() {
  const { questions, doneSet, starSet, categories, toggleDone, toggleStar, resetProgress, loading, error } = useQuestions()

  const [search, setSearch] = useState("")
  const [currentCat, setCurrentCat] = useState("全部")
  const [diffFilter, setDiffFilter] = useState(0)
  const [page, setPage] = useState(1)
  const [mode, setMode] = useState<"list" | "quiz">("list")
  const [showStarred, setShowStarred] = useState(false)
  const [showDoneOnly, setShowDoneOnly] = useState(false)
  const [drawerOpen, setDrawerOpen] = useState(false)

  // Quiz state
  const [quizQuestions, setQuizQuestions] = useState<Question[]>([])
  const [quizIndex, setQuizIndex] = useState(0)
  const [quizShowAnswer, setQuizShowAnswer] = useState(false)

  // Filter
  const filtered = useMemo(() => {
    let qs = questions
    if (currentCat !== "全部") qs = qs.filter((q) => q.category === currentCat)
    if (search) { const s = search.toLowerCase(); qs = qs.filter((q) => q.question.toLowerCase().includes(s)) }
    if (diffFilter > 0) qs = qs.filter((q) => q.difficulty === diffFilter)
    if (showStarred) qs = qs.filter((q) => starSet.has(q.id))
    if (showDoneOnly) qs = qs.filter((q) => doneSet.has(q.id))
    return qs
  }, [questions, currentCat, search, diffFilter, showStarred, showDoneOnly, starSet, doneSet])

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE)
  const paged = useMemo(() => filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE), [filtered, page])

  const visiblePages = useMemo(() => {
    let s = Math.max(1, page - 2), e = Math.min(totalPages, s + 4)
    if (e - s < 4) s = Math.max(1, e - 4)
    return Array.from({ length: e - s + 1 }, (_, i) => s + i)
  }, [page, totalPages])

  const percent = questions.length ? Math.round((doneSet.size / questions.length) * 100) : 0

  // Quiz
  const startQuiz = useCallback(() => {
    setMode("quiz")
    setShowStarred(false)
    setShowDoneOnly(false)
    const qs = filtered.length ? filtered : questions
    const shuffled = [...qs].sort(() => Math.random() - 0.5).slice(0, Math.min(50, qs.length))
    setQuizQuestions(shuffled)
    setQuizIndex(0)
    setQuizShowAnswer(false)
  }, [filtered, questions])

  const currentQuizQ = quizQuestions[quizIndex]

  const goAll = () => { setMode("list"); setShowStarred(false); setShowDoneOnly(false); setCurrentCat("全部"); setPage(1) }
  const goStarred = () => { setMode("list"); setShowStarred(true); setShowDoneOnly(false); setPage(1) }
  const goDone = () => { setMode("list"); setShowDoneOnly(true); setShowStarred(false); setPage(1) }

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (mode !== "quiz") return
      if (e.key === "ArrowRight") { e.preventDefault(); setQuizIndex((i) => Math.min(i + 1, quizQuestions.length - 1)); setQuizShowAnswer(false) }
      else if (e.key === "ArrowLeft") { e.preventDefault(); setQuizIndex((i) => Math.max(i - 1, 0)); setQuizShowAnswer(false) }
      else if (e.key === " ") { e.preventDefault(); setQuizShowAnswer(true) }
      else if (e.key === "Enter" && currentQuizQ) { e.preventDefault(); toggleDone(currentQuizQ.id) }
    }
    document.addEventListener("keydown", handler)
    return () => document.removeEventListener("keydown", handler)
  }, [mode, quizQuestions.length, currentQuizQ, toggleDone])

  // Touch swipe
  const handleTouchStart = (e: React.TouchEvent) => { (e.currentTarget as HTMLElement).dataset.tx = String(e.touches[0].clientX) }
  const handleTouchEnd = (e: React.TouchEvent) => {
    const dx = e.changedTouches[0].clientX - Number((e.currentTarget as HTMLElement).dataset.tx || 0)
    if (Math.abs(dx) > 60) {
      if (dx < 0) { setQuizIndex((i) => Math.min(i + 1, quizQuestions.length - 1)); setQuizShowAnswer(false) }
      else { setQuizIndex((i) => Math.max(i - 1, 0)); setQuizShowAnswer(false) }
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-10 h-10 border-2 border-primary/30 border-t-primary rounded-full animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground text-sm">加载题库中...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="text-center max-w-sm">
          <p className="text-4xl mb-4">😵</p>
          <p className="text-foreground font-medium mb-2">{error}</p>
          <button onClick={() => location.reload()} className="mt-4 px-6 py-2.5 bg-primary text-primary-foreground rounded-xl font-medium">
            刷新页面
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col pb-16 lg:pb-0">
      <Header total={questions.length} done={doneSet.size} starred={starSet.size} percent={percent} />

      <div className="flex flex-1 max-w-[1440px] w-full mx-auto">
        <Sidebar
          categories={categories}
          current={currentCat}
          onSelect={(n) => { setCurrentCat(n); setPage(1) }}
          doneCount={doneSet.size}
          totalCount={questions.length}
          percent={percent}
          onRandomQuiz={startQuiz}
          onReset={resetProgress}
        />

        <main className="flex-1 min-w-0">
          {/* Toolbar */}
          <div className="sticky top-14 sm:top-16 z-40 glass border-b border-border/30 px-3 sm:px-5 py-3">
            <div className="flex flex-col sm:flex-row sm:items-center gap-2.5 sm:gap-3">
              <div className="flex items-center gap-2.5 flex-1">
                <div className="flex bg-card rounded-xl p-1 border border-border/50 shrink-0">
                  <button
                    onClick={() => setMode("list")}
                    className={cn(
                      "flex items-center gap-1.5 px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all",
                      mode === "list" ? "bg-primary/15 text-primary glow-border" : "text-muted-foreground hover:text-foreground"
                    )}
                  >
                    <LayoutList className="w-4 h-4" /> 列表
                  </button>
                  <button
                    onClick={startQuiz}
                    className={cn(
                      "flex items-center gap-1.5 px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all",
                      mode === "quiz" ? "bg-primary/15 text-primary glow-border" : "text-muted-foreground hover:text-foreground"
                    )}
                  >
                    <Target className="w-4 h-4" /> 刷题
                  </button>
                </div>
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <input
                    value={search}
                    onChange={(e) => { setSearch(e.target.value); setPage(1) }}
                    placeholder="搜索题目..."
                    className="w-full pl-9 pr-3 py-2 sm:py-2.5 bg-card border border-border/50 rounded-xl text-xs sm:text-sm text-foreground placeholder:text-muted-foreground/60 outline-none transition-all focus:border-primary/50 focus:shadow-[0_0_16px_oklch(0.75_0.12_260/0.2)]"
                  />
                </div>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  {DIFF_FILTERS.map((d) => (
                    <button
                      key={d.v}
                      onClick={() => { setDiffFilter(d.v); setPage(1) }}
                      className={cn(
                        "w-8 h-8 sm:w-9 sm:h-9 rounded-lg border text-[10px] sm:text-xs font-medium flex items-center justify-center transition-all",
                        diffFilter === d.v
                          ? "bg-primary/15 border-primary/40 text-primary"
                          : "bg-card border-border/50 text-muted-foreground hover:border-primary/30"
                      )}
                    >
                      {d.l}
                    </button>
                  ))}
                </div>
                <button
                  className="lg:hidden flex items-center gap-1.5 px-3 py-2 bg-card border border-border/50 rounded-xl text-xs text-muted-foreground transition-all hover:border-primary/30"
                  onClick={() => setDrawerOpen(true)}
                >
                  <Filter className="w-3.5 h-3.5" />
                  <span className="max-w-[60px] truncate">{currentCat === "全部" ? "分类" : currentCat}</span>
                </button>
                <button
                  className={cn(
                    "lg:hidden w-8 h-8 rounded-lg border flex items-center justify-center text-xs transition-all",
                    showStarred ? "bg-warn/15 border-warn/40 text-warn" : "bg-card border-border/50 text-muted-foreground"
                  )}
                  onClick={() => { setShowStarred(!showStarred); setPage(1) }}
                >
                  <Star className={cn("w-4 h-4", showStarred && "fill-current")} />
                </button>
                <button
                  className={cn(
                    "lg:hidden w-8 h-8 rounded-lg border flex items-center justify-center text-xs transition-all",
                    showDoneOnly ? "bg-success/15 border-success/40 text-success" : "bg-card border-border/50 text-muted-foreground"
                  )}
                  onClick={() => { setShowDoneOnly(!showDoneOnly); setPage(1) }}
                >
                  ✓
                </button>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="p-3 sm:p-5">
            {/* LIST MODE */}
            {mode === "list" && (
              <>
                {paged.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-16 sm:py-20 text-muted-foreground">
                    <Search className="w-12 h-12 mb-4 opacity-30" />
                    <p className="text-base sm:text-lg">没有找到匹配的题目</p>
                    <p className="text-xs sm:text-sm mt-1">试试其他关键词或分类</p>
                  </div>
                ) : (
                  <div className="space-y-2 sm:space-y-2.5">
                    {paged.map((q, i) => (
                      <QuestionCard
                        key={q.id}
                        question={q}
                        index={i}
                        isDone={doneSet.has(q.id)}
                        isStarred={starSet.has(q.id)}
                        onToggleDone={() => toggleDone(q.id)}
                        onToggleStar={() => toggleStar(q.id)}
                      />
                    ))}
                  </div>
                )}

                {totalPages > 1 && (
                  <div className="flex items-center justify-center gap-1 sm:gap-1.5 mt-5 sm:mt-6 py-3">
                    <button
                      disabled={page === 1}
                      onClick={() => setPage(page - 1)}
                      className="w-9 h-9 rounded-lg border border-border/50 bg-card text-muted-foreground flex items-center justify-center transition-all hover:border-primary/30 hover:text-primary disabled:opacity-20 disabled:cursor-not-allowed active:scale-95"
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </button>
                    {visiblePages.map((p) => (
                      <button
                        key={p}
                        onClick={() => setPage(p)}
                        className={cn(
                          "min-w-[32px] sm:min-w-[36px] h-9 rounded-lg border text-xs sm:text-sm font-mono flex items-center justify-center transition-all active:scale-95",
                          page === p
                            ? "bg-primary border-primary text-primary-foreground glow-border"
                            : "border-border/50 bg-card text-muted-foreground hover:border-primary/30 hover:text-primary"
                        )}
                      >
                        {p}
                      </button>
                    ))}
                    <button
                      disabled={page === totalPages}
                      onClick={() => setPage(page + 1)}
                      className="w-9 h-9 rounded-lg border border-border/50 bg-card text-muted-foreground flex items-center justify-center transition-all hover:border-primary/30 hover:text-primary disabled:opacity-20 disabled:cursor-not-allowed active:scale-95"
                    >
                      <ChevronRight className="w-4 h-4" />
                    </button>
                    <span className="text-muted-foreground text-[10px] sm:text-xs font-mono ml-1 sm:ml-2 hidden sm:inline">
                      {page}/{totalPages} · {filtered.length}题
                    </span>
                  </div>
                )}
              </>
            )}

            {/* QUIZ MODE */}
            {mode === "quiz" && (
              <>
                {quizQuestions.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-16 sm:py-20 text-muted-foreground">
                    <Target className="w-12 h-12 mb-4 opacity-30" />
                    <p className="text-base sm:text-lg">没有符合条件的题目</p>
                    <button onClick={startQuiz} className="mt-4 px-6 py-2.5 bg-primary text-primary-foreground rounded-xl font-medium glow-border hover:brightness-110 transition-all">
                      重新加载
                    </button>
                  </div>
                ) : (
                  <div className="max-w-[700px] mx-auto" onTouchStart={handleTouchStart} onTouchEnd={handleTouchEnd}>
                    <div className="flex items-center justify-between mb-3 sm:mb-4">
                      <span className="text-muted-foreground text-xs font-mono">{quizIndex + 1} / {quizQuestions.length}</span>
                      <div className="flex gap-1">
                        {Array.from({ length: 4 }, (_, i) => (
                          <span key={i} className={cn("text-xs sm:text-sm", i < (currentQuizQ?.difficulty || 0) ? "text-warn" : "text-border")}>★</span>
                        ))}
                      </div>
                    </div>

                    {currentQuizQ && (
                      <motion.div
                        key={quizIndex}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.2 }}
                        className="bg-card/60 border border-border/50 rounded-2xl p-5 sm:p-8 hover:shadow-[0_0_40px_oklch(0.7_0.14_250/0.08)] transition-all duration-300 hover:border-primary/20"
                      >
                        <div className="text-base sm:text-lg leading-relaxed font-medium text-foreground mb-4 sm:mb-6">
                          {currentQuizQ.question}
                        </div>
                        {quizShowAnswer && (
                          <motion.div
                            initial={{ opacity: 0, y: 8 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="bg-background/50 border border-border/30 rounded-xl p-4 sm:p-5"
                          >
                            <div className="flex items-center gap-2 text-success text-[10px] sm:text-[11px] font-bold uppercase tracking-wider mb-2 sm:mb-3">
                              💡 参考答案
                            </div>
                            <div className="text-[13px] sm:text-sm leading-relaxed text-muted-foreground whitespace-pre-wrap">
                              {currentQuizQ.answer}
                            </div>
                          </motion.div>
                        )}
                      </motion.div>
                    )}

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3 mt-4 sm:mt-5">
                      <button
                        disabled={quizIndex === 0}
                        onClick={() => { setQuizIndex((i) => i - 1); setQuizShowAnswer(false) }}
                        className="px-4 py-3 sm:py-2.5 rounded-xl border border-border/50 bg-card text-muted-foreground text-xs sm:text-sm font-medium transition-all hover:border-primary/30 hover:text-foreground disabled:opacity-20 disabled:cursor-not-allowed active:scale-95"
                      >
                        ← 上一题
                      </button>
                      {!quizShowAnswer ? (
                        <button
                          onClick={() => setQuizShowAnswer(true)}
                          className="px-4 py-3 sm:py-2.5 bg-primary text-primary-foreground rounded-xl font-medium text-xs sm:text-sm glow-border hover:brightness-110 transition-all active:scale-95"
                        >
                          显示答案
                        </button>
                      ) : (
                        <button
                          onClick={() => currentQuizQ && toggleDone(currentQuizQ.id)}
                          className={cn(
                            "px-4 py-3 sm:py-2.5 rounded-xl border text-xs sm:text-sm font-medium transition-all active:scale-95",
                            currentQuizQ && doneSet.has(currentQuizQ.id)
                              ? "border-success/40 bg-success/10 text-success"
                              : "border-border/50 bg-card text-muted-foreground hover:border-primary/30"
                          )}
                        >
                          {currentQuizQ && doneSet.has(currentQuizQ.id) ? "✓ 已掌握" : "标记掌握"}
                        </button>
                      )}
                      <button
                        onClick={() => currentQuizQ && toggleDone(currentQuizQ.id)}
                        className={cn(
                          "px-4 py-3 sm:py-2.5 rounded-xl border text-xs sm:text-sm font-medium transition-all active:scale-95",
                          currentQuizQ && doneSet.has(currentQuizQ.id)
                            ? "border-success/40 bg-success/10 text-success"
                            : "border-border/50 bg-card text-muted-foreground hover:border-primary/30"
                        )}
                      >
                        {currentQuizQ && doneSet.has(currentQuizQ.id) ? "✓ 已掌握" : "标记掌握"}
                      </button>
                      <button
                        disabled={quizIndex >= quizQuestions.length - 1}
                        onClick={() => { setQuizIndex((i) => i + 1); setQuizShowAnswer(false) }}
                        className="px-4 py-3 sm:py-2.5 rounded-xl border border-border/50 bg-card text-muted-foreground text-xs sm:text-sm font-medium transition-all hover:border-primary/30 hover:text-foreground disabled:opacity-20 disabled:cursor-not-allowed active:scale-95"
                      >
                        下一题 →
                      </button>
                    </div>
                    <p className="text-center text-[10px] sm:text-[11px] text-muted-foreground/40 mt-3 sm:mt-4">
                      <span className="sm:hidden">← 左滑下一题 · 右滑上一题 · 点击看答案</span>
                      <span className="hidden sm:inline">快捷键：← → 切换 · 空格 显示答案 · Enter 标记掌握</span>
                    </p>
                  </div>
                )}
              </>
            )}
          </div>
        </main>
      </div>

      <BottomNav
        mode={mode}
        showStarred={showStarred}
        showDoneOnly={showDoneOnly}
        onAll={goAll}
        onStarred={goStarred}
        onDone={goDone}
        onQuiz={startQuiz}
      />

      <CategoryDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        categories={categories}
        current={currentCat}
        onSelect={(n) => { setCurrentCat(n); setPage(1) }}
        onRandomQuiz={startQuiz}
        onReset={resetProgress}
      />
    </div>
  )
}
