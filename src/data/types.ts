export interface Question {
  id: number
  question: string
  category: string
  difficulty: number
  answer: string
}

export interface CategoryInfo {
  name: string
  icon: string
  count: number
}

export const CATEGORY_ICONS: Record<string, string> = {
  "全部": "📋",
  "Java基础": "☕",
  "集合框架": "📦",
  "多线程与并发": "🧵",
  "JVM": "⚙️",
  "Spring": "🌱",
  "SpringBoot": "🚀",
  "SpringCloud": "☁️",
  "MyBatis": "🗃️",
  "MySQL": "🐬",
  "Redis": "🔴",
  "消息队列": "📨",
  "Elasticsearch": "🔍",
  "Docker与DevOps": "🐳",
  "设计模式": "🏗️",
  "项目与场景": "💼",
  "MongoDB与NoSQL": "🍃",
  "分布式": "🔗",
  "HR与软技能": "👔",
  "其他": "📌",
}
