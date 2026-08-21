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
  const [allLoaded, setAllLoaded] = useState(false)
  const [allLoading, setAllLoading] = useState(false)
  const [categoryData, setCategoryData] = useState<Map<string, Question[]>>(new Map())
  const [catIndex, setCatIndex] = useState<{ name: string; count: number; file: string }[]>([])
  const [doneSet, setDoneSet] = useState<Set<number>>(() => loadSet(STORAGE_DONE))
  const [starSet, setStarSet] = useState<Set<number>>(() => loadSet(STORAGE_STAR))
  const [loading, setLoading] = useState(true)
  const [loadingCat, setLoadingCat] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Step 1: Load index
  useEffect(() => {
    fetch(BASE + "data/index.json")
      .then((r) => r.json())
      .then((index) => {
        setCatIndex(index)
        setLoading(false)
      })
      .catch((e) => {
        console.error("[useQuestions] index failed:", e)
        setError("题库索引加载失败")
        setLoading(false)
      })
  }, [])

  // Step 2: Load full data (streaming-style: show first category fast, load rest in background)
  const loadAllQuestions = useCallback(async () => {
    if (allLoaded || allLoading) return allQuestions
    setAllLoading(true)
    try {
      const r = await fetch(BASE + "data.json")
      const raw = await r.json()
      const qs = decompress(raw)
      setAllQuestions(qs)
      setAllLoaded(true)
      setAllLoading(false)
      return qs
    } catch (e) {
      console.error("[useQuestions] full data failed:", e)
      setAllLoading(false)
      return []
    }
  }, [allLoaded, allLoading, allQuestions])

  // Load specific category on demand
  const loadCategory = useCallback(async (catName: string): Promise<Question[]> => {
    if (catName === "全部") {
      return await loadAllQuestions()
    }
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
  }, [categoryData, catIndex, loadAllQuestions])

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

  const categories: CategoryInfo[] = [
    { name: "全部", icon: "📋", count: catIndex.reduce((s, c) => s + c.count, 0) },
    ...catIndex.map((c) => ({ name: c.name, icon: CATEGORY_ICONS[c.name] || "📌", count: c.count })),
  ]

  return {
    allQuestions, allLoaded, allLoading, categoryData, catIndex, categories,
    doneSet, starSet, loading, loadingCat, error,
    loadCategory, loadAllQuestions, toggleDone, toggleStar, resetProgress,
  }
}
