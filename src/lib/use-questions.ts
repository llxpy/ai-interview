import { useState, useEffect, useCallback, useRef } from "react"
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
  const [categoryData, setCategoryData] = useState<Map<string, Question[]>>(new Map())
  const [catIndex, setCatIndex] = useState<{ name: string; count: number; file: string }[]>([])
  const [doneSet, setDoneSet] = useState<Set<number>>(() => loadSet(STORAGE_DONE))
  const [starSet, setStarSet] = useState<Set<number>>(() => loadSet(STORAGE_STAR))
  const [loading, setLoading] = useState(true)
  const [loadingCat, setLoadingCat] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const loadingRef = useRef<Set<string>>(new Set())

  // Load index on mount
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

  // Load a single category file
  const loadCategoryFile = useCallback(async (catName: string): Promise<Question[]> => {
    if (categoryData.has(catName)) return categoryData.get(catName)!
    if (loadingRef.current.has(catName)) return []

    const entry = catIndex.find((c) => c.name === catName)
    if (!entry) return []

    loadingRef.current.add(catName)
    try {
      const r = await fetch(BASE + entry.file)
      const raw = await r.json()
      const qs = decompress(raw)
      setCategoryData((prev) => new Map(prev).set(catName, qs))
      loadingRef.current.delete(catName)
      return qs
    } catch (e) {
      console.error("[loadCategoryFile] failed:", catName, e)
      loadingRef.current.delete(catName)
      return []
    }
  }, [categoryData, catIndex])

  // Load a category (single file or "全部" = all files)
  const loadCategory = useCallback(async (catName: string): Promise<Question[]> => {
    if (catName === "全部") {
      // Load all unloaded categories and merge
      setLoadingCat(true)
      const promises = catIndex.map(async (c) => {
        if (categoryData.has(c.name)) return categoryData.get(c.name)!
        return await loadCategoryFile(c.name)
      })
      const results = await Promise.all(promises)
      const all = results.flat()
      setLoadingCat(false)
      return all
    }
    setLoadingCat(true)
    const qs = await loadCategoryFile(catName)
    setLoadingCat(false)
    return qs
  }, [catIndex, categoryData, loadCategoryFile])

  // Get questions for a category (from cache or empty)
  const getQuestions = useCallback((catName: string): Question[] => {
    if (catName === "全部") {
      return Array.from(categoryData.values()).flat()
    }
    return categoryData.get(catName) || []
  }, [categoryData])

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

  // Dynamic categories: counts from actual loaded data, fallback to index counts
  const categories: CategoryInfo[] = (() => {
    const loadedCounts: Record<string, number> = {}
    for (const [name, qs] of categoryData) {
      loadedCounts[name] = qs.length
    }
    const totalCount = catIndex.reduce((s, c) => s + c.count, 0)
    const loadedTotal = Object.values(loadedCounts).reduce((s, n) => s + n, 0)
    return [
      { name: "全部", icon: "📋", count: loadedTotal > 0 ? loadedTotal : totalCount },
      ...catIndex.map((c) => ({
        name: c.name,
        icon: CATEGORY_ICONS[c.name] || "📌",
        count: loadedCounts[c.name] ?? c.count,
      })),
    ]
  })()

  return {
    categoryData, catIndex, categories,
    doneSet, starSet, loading, loadingCat, error,
    loadCategory, loadCategoryFile, getQuestions,
    toggleDone, toggleStar, resetProgress,
  }
}
