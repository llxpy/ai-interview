import { useState, useEffect, useCallback } from "react"
import type { Question, CategoryInfo } from "@/data/types"
import { CATEGORY_ICONS } from "@/data/types"

const STORAGE_DONE = "ai_done"
const STORAGE_STAR = "ai_star"

function loadSet(key: string): Set<number> {
  try {
    return new Set(JSON.parse(localStorage.getItem(key) || "[]"))
  } catch {
    return new Set()
  }
}

export function useQuestions() {
  const [questions, setQuestions] = useState<Question[]>([])
  const [doneSet, setDoneSet] = useState<Set<number>>(() => loadSet(STORAGE_DONE))
  const [starSet, setStarSet] = useState<Set<number>>(() => loadSet(STORAGE_STAR))

  useEffect(() => {
    fetch("data.json")
      .then((r) => r.json())
      .then(setQuestions)
      .catch(() => {
        // fallback: try with base URL
        fetch(import.meta.env.BASE_URL + "data.json")
          .then((r) => r.json())
          .then(setQuestions)
          .catch(console.error)
      })
  }, [])

  useEffect(() => {
    localStorage.setItem(STORAGE_DONE, JSON.stringify([...doneSet]))
  }, [doneSet])

  useEffect(() => {
    localStorage.setItem(STORAGE_STAR, JSON.stringify([...starSet]))
  }, [starSet])

  const toggleDone = useCallback(
    (id: number) => setDoneSet((prev) => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n }),
    []
  )
  const toggleStar = useCallback(
    (id: number) => setStarSet((prev) => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n }),
    []
  )
  const resetProgress = useCallback(() => {
    setDoneSet(new Set())
    setStarSet(new Set())
  }, [])

  const categories: CategoryInfo[] = (() => {
    const counts: Record<string, number> = {}
    questions.forEach((q) => { counts[q.category] = (counts[q.category] || 0) + 1 })
    const cats = Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .map(([name, count]) => ({ name, icon: CATEGORY_ICONS[name] || "📌", count }))
    return [{ name: "全部", icon: "📋", count: questions.length }, ...cats]
  })()

  return { questions, doneSet, starSet, categories, toggleDone, toggleStar, resetProgress }
}
