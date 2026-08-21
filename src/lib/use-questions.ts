import { useState, useEffect, useCallback } from "react"
import type { Question, CategoryInfo } from "@/data/types"
import { CATEGORY_ICONS } from "@/data/types"

const STORAGE_DONE = "ai_done"
const STORAGE_STAR = "ai_star"
const BASE = import.meta.env.BASE_URL || "/"

function loadSet(key: string): Set<number> {
  try {
    return new Set(JSON.parse(localStorage.getItem(key) || "[]"))
  } catch {
    return new Set()
  }
}

// Decompress: short keys → full Question
function decompress(raw: Record<string, unknown>[]): Question[] {
  return raw.map((r) => ({
    id: r["i"] as number,
    question: r["q"] as string,
    category: r["c"] as string,
    difficulty: r["d"] as number,
    answer: r["a"] as string,
  }))
}

export function useQuestions() {
  const [allQuestions, setAllQuestions] = useState<Question[]>([])
  const [categoryData, setCategoryData] = useState<Map<string, Question[]>>(new Map())
  const [catIndex, setCatIndex] = useState<{ name: string; count: number; file: string }[]>([])
  const [doneSet, setDoneSet] = useState<Set<number>>(() => loadSet(STORAGE_DONE))
  const [starSet, setStarSet] = useState<Set<number>>(() => loadSet(STORAGE_STAR))
  const [loading, setLoading] = useState(true)
  const [loadingCat, setLoadingCat] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Load category index + "其他" category as initial
  useEffect(() => {
    console.log("[useQuestions] loading index...")
    fetch(BASE + "data/index.json")
      .then((r) => r.json())
      .then((index) => {
        setCatIndex(index)
        // Load full data.json for "全部" view (lazy, non-blocking)
        fetch(BASE + "data.json")
          .then((r) => r.json())
          .then((raw) => {
            console.log("[useQuestions] full data loaded:", raw.length)
            setAllQuestions(decompress(raw))
            setLoading(false)
          })
          .catch((e) => {
            console.error("[useQuestions] full data failed:", e)
            setError("题库加载失败，请刷新重试")
            setLoading(false)
          })
      })
      .catch((e) => {
        console.error("[useQuestions] index failed:", e)
        setError("题库索引加载失败")
        setLoading(false)
      })
  }, [])

  // Load specific category on demand
  const loadCategory = useCallback(async (catName: string): Promise<Question[]> => {
    if (catName === "全部") return allQuestions
    if (categoryData.has(catName)) return categoryData.get(catName)!

    const entry = catIndex.find((c) => c.name === catName)
    if (!entry) return []

    setLoadingCat(true)
    try {
      const r = await fetch(BASE + entry.file)
      const raw = await r.json()
      const qs = decompress(raw)
      setCategoryData((prev) => new Map(prev).set(catName, qs))
      setLoadingCat(false)
      return qs
    } catch (e) {
      console.error("[loadCategory] failed:", catName, e)
      setLoadingCat(false)
      return []
    }
  }, [allQuestions, categoryData, catIndex])

  // Persist
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

  // Build categories from index
  const categories: CategoryInfo[] = [
    { name: "全部", icon: "📋", count: catIndex.reduce((s, c) => s + c.count, 0) },
    ...catIndex.map((c) => ({ name: c.name, icon: CATEGORY_ICONS[c.name] || "📌", count: c.count })),
  ]

  return {
    allQuestions, categoryData, catIndex, categories,
    doneSet, starSet, loading, loadingCat, error,
    loadCategory, toggleDone, toggleStar, resetProgress,
  }
}
