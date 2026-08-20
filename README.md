# AI面试宝典

> 18,095 道真实面试题 · 渐进式刷题系统

从真实面试记录中提取的 Java 后端面试题库，覆盖 19 个技术分类，支持列表浏览、搜索过滤、随机刷题、进度追踪。

**🔗 在线访问：https://llxpy.github.io/ai-interview/**

## 功能

- 📋 **列表模式** — 分类浏览、关键词搜索、难度筛选、展开查看参考答案
- 🎯 **刷题模式** — 随机抽题 50 道，支持键盘快捷键（←→ 切题 / 空格看答案 / Enter 标记掌握）
- ⭐ **收藏 & 掌握** — 标记收藏和已掌握，localStorage 持久化
- 📱 **手机适配** — 底部导航栏、分类抽屉、左右滑动切题、触控友好
- 🎨 **暗色主题** — 与 [llxpy-blog](https://llxpy.github.io/llxpy-blog/) 同款 oklch 色系

## 技术栈

| 层 | 技术 |
|---|------|
| 框架 | React 19 + TypeScript 5.9 |
| 构建 | Vite 7 |
| 样式 | Tailwind CSS v4 |
| 动画 | Framer Motion |
| 图标 | Lucide React |
| 部署 | GitHub Actions → GitHub Pages |

## 本地开发

```bash
npm install
npm run dev      # 启动开发服务器
npm run build    # 构建生产版本
npm run preview  # 预览构建产物
```

## 添加题库

编辑 `public/data.json`，每道题的格式：

```json
{
  "id": 1,
  "question": "题目内容",
  "category": "分类名称",
  "difficulty": 2,
  "answer": "参考答案"
}
```

- **difficulty**：1~4（★ ~ ★★★★）
- **category**：已有分类见 `src/data/types.ts` 中的 `CATEGORY_ICONS`

修改后 push 到 main 分支，GitHub Actions 自动部署。

## 题目分布

| 分类 | 数量 |
|------|------|
| Spring | 2,320 |
| MySQL | 1,828 |
| 多线程与并发 | 1,715 |
| 项目与场景 | 1,264 |
| Java基础 | 1,081 |
| 集合框架 | 804 |
| SpringCloud | 614 |
| JVM | 605 |
| 消息队列 | 587 |
| Elasticsearch | 440 |
| HR与软技能 | 439 |
| Docker与DevOps | 433 |
| Redis | 223 |
| MyBatis | 186 |
| 设计模式 | 83 |
| 分布式 | 82 |
| MongoDB与NoSQL | 37 |
| SpringBoot | 22 |

## License

MIT
