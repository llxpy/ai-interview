import json, re

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Re-classify "其他" questions and give real answers
tech_answers = {
    # SQL/数据库
    "左连接": "LEFT JOIN(左连接)：返回左表所有行,右表无匹配则填NULL。RIGHT JOIN(右连接)：返回右表所有行。FULL JOIN(全连接)：返回两表所有行,无匹配则填NULL。INNER JOIN(内连接)：只返回两表都匹配的行。MySQL不支持FULL JOIN,可用UNION模拟。",
    "连接.*查询": "JOIN类型：INNER JOIN(两表匹配行)/LEFT JOIN(左表全部+右表匹配)/RIGHT JOIN(右表全部)/CROSS JOIN(笛卡尔积)。MySQL无FULL JOIN,用LEFT JOIN UNION RIGHT JOIN模拟。性能：JOIN字段加索引,小表驱动大表。",
    "两张表.*查询": "多表查询：①JOIN(关联查询,推荐) ②子查询(嵌套SELECT) ③UNION(合并结果集)。JOIN性能通常优于子查询。关联字段必须加索引。",
    "相同的数据": "查询两表相同数据：①INNER JOIN(两表关联取交集) ②IN/EXISTS子查询 ③INTERSECT(MySQL不支持,用JOIN模拟)。去重：SELECT DISTINCT。交集/并集/差集：INTERSECT/UNION/EXCEPT。",
    "数据库表设计": "表设计原则：①三大范式(1NF原子性/2NF完全依赖/3NF消除传递依赖) ②适当反范式(冗余字段提升查询) ③主键选择(自增整数,雪花算法) ④字段类型(能用小的不用大的) ⑤索引设计(高频查询字段建索引) ⑥注释(表和字段必须有COMMENT)。",
    "分表.*失效": "分库分表后索引失效的场景：①跨分片查询(需要聚合多个分片) ②非分片键查询(无法路由到特定分片) ③JOIN跨分片(需要应用层关联) ④排序/分页跨分片(需要各分片排序后合并)。解决：分片键选择(高频查询字段)/全局表(小表广播)/ER分片(关联表同分片)。",

    # 前端
    "vue": "Vue.js渐进式前端框架。核心：①响应式数据(Proxy劫持getter/setter) ②组件化(SFC单文件组件) ③虚拟DOM(Diff算法高效更新) ④指令(v-if/v-for/v-model/v-show) ⑤组合式API(Composition API,setup函数)。Vue3：Proxy替代defineProperty/Teleport/Suspense/更好的TS支持。构建工具：Vite(推荐)/Webpack。",
    "react": "React前端框架。核心：①JSX(JavaScript+XML语法) ②组件(函数组件+Hooks) ③虚拟DOM ④单向数据流。Hooks：useState(状态)/useEffect(副作用)/useContext(上下文)/useMemo(缓存)/useCallback(缓存函数)。状态管理：Redux/Zustand/Jotai。构建：Vite/Next.js(SSR)。",
    "前端": "前端技术栈：①HTML/CSS/JavaScript基础 ②框架(Vue/React/Angular) ③构建工具(Vite/Webpack) ④CSS方案(Tailwind/SCSS/CSS Modules) ⑤状态管理(Pinia/Redux) ⑥路由(Vue Router/React Router) ⑦HTTP(Axios/Fetch) ⑧UI库(Element Plus/Ant Design)。TypeScript是趋势。",
    "v-if": "Vue中v-if和v-show区别：v-if是条件渲染(不满足条件则DOM不存在,切换开销大)。v-show是CSS display切换(DOM始终存在,切换开销小)。频繁切换用v-show,运行条件很少改变用v-if。v-if可配合v-else-if/v-else链式使用。",
    "v-for": "Vue中v-for列表渲染：v-for=\"(item, index) in list\"。必须加:key(唯一标识,用id而非index)。数组更新检测：变异方法(push/pop/splice/sort)触发视图更新。直接赋值(arr[index]=val)不触发,用Vue.set或splice替代。",

    # 算法/数据结构
    "红黑树": "自平衡二叉搜索树。性质：①节点红或黑 ②根节点黑 ③叶子(NIL)黑 ④红节点的子节点必须黑 ⑤从任一节点到叶子的所有路径黑节点数相同。保证最长路径不超过最短路径2倍,查找/插入/删除都是O(log n)。Java中TreeMap/TreeSet使用红黑树,HashMap链表长度≥8时转红黑树。",
    "冒泡排序": "相邻元素两两比较,大的往后移。时间复杂度：O(n²)(最坏/平均),O(n)(最好,已排序时优化版)。空间O(1),稳定排序。优化：①记录最后交换位置(之后的已有序) ②双向冒泡(鸡尾酒排序)。面试常考,但实际开发用Arrays.sort()。",
    "排序": "常见排序算法：①冒泡O(n²)稳定 ②选择O(n²)不稳定 ③插入O(n²)稳定 ④希尔O(n^1.3)不稳定 ⑤归并O(n log n)稳定 ⑥快速O(n log n)平均/不稳定 ⑦堆O(n log n)不稳定 ⑧计数/桶/基数O(n+k)。Arrays.sort()：基本类型用双轴快排,对象类型用TimSort(归并+插入)。",
    "二分查找": "在有序数组中查找目标值。时间O(log n),空间O(1)。实现：left=0, right=n-1, while(left<=right){mid=(left+right)/2; if(arr[mid]==target)return mid; else if(arr[mid]<target)left=mid+1; else right=mid-1;}。变体：查找第一个/最后一个等于目标的位置。Arrays.binarySearch()。",
    "链表": "单链表(每个节点指向下一个)/双向链表(前驱+后继)/循环链表(尾指向头)。操作：查找O(n),头插O(1),中间插入O(n)(需先找到位置)。vs数组：链表动态大小/插入删除O(1)(已知位置)/但随机访问O(n)/缓存不友好。Java中LinkedList是双向链表。",
    "栈": "后进先出(LIFO)。操作：push(入栈)/pop(出栈)/peek(查看栈顶)。Java中Stack类(不推荐,用Deque替代)/ArrayDeque(推荐)。应用：括号匹配/表达式求值/DFS/浏览器后退/方法调用栈。",
    "队列": "先进先出(FIFO)。操作：offer(入队)/poll(出队)/peek(查看队头)。变体：双端队列(Deque,两端都可进出)/优先队列(PriorityQueue,堆实现,按优先级出队)/循环队列。ArrayDeque(数组双端队列)/LinkedList(链式双端队列)/PriorityQueue(优先队列)。",
    "树": "二叉树(每个节点最多两个子节点)/BST(左<根<右)/AVL(严格平衡)/红黑树(近似平衡)/B+树(MySQL索引)/字典树(Trie,字符串检索)/线段树(区间查询)。遍历：前序(根-左-右)/中序(左-根-右)/后序(左-右-根)/层序(BFS)。递归或栈实现。",
    "图": "有向图/无向图/加权图。存储：邻接矩阵(空间O(V²))/邻接表(空间O(V+E))。遍历：BFS(队列,最短路径)/DFS(栈/递归,连通性)。最短路径：Dijkstra(非负权)/Bellman-Ford(可负权)/Floyd(全源最短路)。拓扑排序：DAG+入度法/Kahn算法。",
    "动态规划": "将问题分解为子问题,保存子问题结果避免重复计算。步骤：①定义状态(dp[i]的含义) ②状态转移方程(dp[i]与dp[i-1]的关系) ③初始条件 ④遍历顺序。经典：斐波那契/背包/最长公共子序列/最长递增子序列/编辑距离/爬楼梯。vs贪心：DP考虑所有子问题,贪心只选当前最优。",
    "递归": "函数调用自身。要素：①终止条件(基准情况) ②递推关系(大问题→小问题) ③返回值。风险：栈溢出(递归太深)。优化：①尾递归(编译器优化) ②记忆化(缓存已计算结果) ③改迭代(手动维护栈)。应用：树遍历/分治/回溯/DFS。",
    "哈希": "哈希表：通过哈希函数将key映射到数组索引,实现O(1)查找。冲突解决：①链地址法(Java HashMap) ②开放寻址法(线性探测/二次探测) ③再哈希。好的哈希函数：均匀分布/计算快。Java HashMap：key.hashCode()高16位异或低16位→(容量-1)&hash。",

    # 设计/架构
    "设计模式": "23种GoF设计模式分三类：①创建型(单例/工厂/抽象工厂/建造者/原型) ②结构型(适配器/桥接/组合/装饰器/外观/享元/代理) ③行为型(责任链/命令/迭代器/中介者/备忘录/观察者/状态/策略/模板方法/访问者)。面试重点：单例(5种实现)/工厂/代理(AOP)/策略/模板方法/观察者。",
    "微服务": "将单体应用拆分为多个独立服务。优势：独立部署/技术异构/故障隔离。挑战：分布式复杂性/服务间通信/数据一致性。拆分原则：按业务领域(DDD)/单一职责/数据独立。通信：同步(HTTP/RPC)/异步(MQ)。架构：API Gateway+注册中心+配置中心+链路追踪。",
    "架构": "常见架构：①单体(所有功能在一个应用,简单但难扩展) ②微服务(拆分为独立服务,灵活但复杂) ③SOA(面向服务,ESB总线) ④Serverless(函数即服务,按调用付费)。选型：小团队/初期→单体 中大型→微服务 事件驱动→Serverless。微服务关键：服务治理/链路追踪/日志聚合/配置中心。",

    # 编程题
    "编程实现": "编程面试题准备：①理解题意(确认输入输出/边界条件) ②想思路(暴力→优化) ③写代码(变量命名清晰/注释关键步骤) ④测试(正常/边界/异常case) ⑤分析复杂度(时间/空间)。刷题平台：LeetCode(算法)/牛客(面试题)。常见题型：数组/字符串/链表/树/DP/排序/查找。",
    "不用equals": "不用equals判断字符串相等：①逐字符比较(for循环charAt) ②compareTo返回0 ③Objects.equals()(null安全) ④hashCode比较(可能哈希碰撞) ⑤字节数组比较(getBytes)。最可靠：逐字符比较。注意：==比较引用地址(不同对象返回false,除非intern()放入常量池)。",

    # 工具/中间件
    "canal": "Canal是阿里开源的MySQL binlog增量订阅&消费组件。原理：伪装MySQL从库→接收binlog→解析→投递到MQ/ES/Redis等。用途：①数据库同步(MySQL→ES/Redis) ②数据仓库ETL ③缓存一致性(Canal+MQ更新Redis)。配置：MySQL开启binlog(row格式)→Canal连接→消费端监听。比双写更可靠(不侵入业务代码)。",
    "布隆过滤器": "概率型数据结构,判断元素是否\"可能存在\"或\"一定不存在\"。原理：多个哈希函数+位数组。添加：对元素做k次哈希,将对应位设为1。查询：所有对应位都是1→\"可能存在\" 有0→\"一定不存在\"。有假阳性(无假阴性)。应用：①Redis防缓存穿透 ②爬虫URL去重 ③邮件反垃圾。Redis有RedisBloom模块。",
    "httpclient": "Java HTTP客户端。①HttpURLConnection(JDK原生,繁琐) ②Apache HttpClient(功能丰富,连接池) ③OkHttp(Square,简洁高效) ④RestTemplate(Spring,同步) ⑤WebClient(Spring WebFlux,异步响应式) ⑥Feign(声明式,微服务间调用)。推荐：微服务用Feign,普通HTTP用OkHttp/RestTemplate。",
    "支付": "支付对接：①支付宝SDK(当面付/APP支付/网页支付/小程序支付) ②微信支付(Native/JSAPI/H5/小程序) ③银联。流程：①创建订单→调支付接口→生成支付链接/二维码 ②用户支付→支付平台回调通知 ③验证签名→更新订单状态。关键：①签名验证(防伪造) ②幂等(回调可能重复) ③对账(定时核对)。",
    "超卖": "库存超卖解决方案：①数据库乐观锁(UPDATE SET stock=stock-1 WHERE id=? AND stock>0,检查影响行数) ②Redis原子操作(DECR库存key,返回值>=0则成功) ③分布式锁(Redis SETNX,扣减前加锁) ④队列削峰(请求入队,单线程消费扣减)。推荐：Redis预扣+数据库最终扣减(Redis做高并发入口,异步同步到DB)。",
    "点赞": "点赞数据存储：①关系型(MySQL)：like表(user_id+target_id+target_type+create_time),联合索引查是否已赞 ②Redis：SET类型(SADD target:likes user_id,SISMEMBER判断)或BITMAP(BITOFFSET user_id)。计数：Redis INCR/DECR原子操作。高频场景用Redis,定时同步到MySQL。取消赞：SREM/DECR。",
    "审核": "内容审核流程：①提交内容→状态设为\"待审核\" ②自动审核(关键词过滤/AI模型分类/第三方审核API如阿里云内容安全) ③自动通过→发布/自动拒绝→通知/不确定→进入人工队列 ④人工审核(审核员查看→通过/拒绝+原因) ⑤结果通知用户。设计：审核表(content_id/status/reviewer/reason/create_time)。",
    "日志": "日志查询方案：①小量：MySQL按时间分区(按天/月分表) ②中量：Elasticsearch(全文检索+时间范围查询) ③大量：ELK(Elasticsearch+Logstash+Kibana)/Loki+Grafana。设计：日志表按时间分区+定期归档。索引：时间字段+用户ID。查询：指定时间范围+关键词搜索。保留策略：热数据SSD+冷数据HDD/对象存储。",

    # Java核心
    "静态": "static关键字。静态变量(类级别,所有实例共享,类加载时初始化)。静态方法(不能访问非静态成员,不能用this/super)。静态内部类(不持有外部类引用,只能访问外部静态成员)。静态代码块(类加载时执行一次)。静态导入(import static)。应用：工具类方法/单例(饿汉式)/常量定义。",
    "Stream": "Java 8 Stream API。创建：list.stream()/Stream.of()/Arrays.stream()。中间操作(惰性)：filter(过滤)/map(映射)/sorted(排序)/distinct(去重)/limit/skip/flatMap。终止操作：forEach/collect(Collectors.toList())/count/reduce/min/max/anyMatch/allMatch。并行流：parallelStream()(ForkJoinPool)。注意：Stream只能消费一次。",
    "Lambda": "Java 8 Lambda表达式,函数式接口的简写。语法：(参数) -> 表达式 或 (参数) -> { 语句; }。函数式接口(只有一个抽象方法)：Function<T,R>(T→R)/Predicate<T>(T→boolean)/Consumer<T>(T→void)/Supplier<T>(()→T)。方法引用：类::静态方法/对象::实例方法/类::new。底层：invokedynamic指令+匿名内部类(首次)/直接调用(后续)。",
    "接口.*默认方法": "JDK8接口新增：①default方法(有实现体,实现类可不重写) ②static方法(接口级别静态方法)。目的：向后兼容(给接口加新方法不破坏已有实现)。冲突：类实现多个接口有同名default方法→必须重写解决冲突。抽象类vs接口：抽象类有状态/构造器,接口没有(但有default方法)。",

    # 场景题
    "响应.*慢": "排查慢请求：①看日志(确认哪个环节慢) ②数据库(慢查询日志,EXPLAIN分析) ③网络(ping/traceroute) ④代码(方法耗时埋点/Arthas trace) ⑤GC(频繁Full GC导致STW) ⑥线程(jstack查看是否有死锁/阻塞) ⑦资源(CPU/内存/IO监控)。工具：Arthas(在线诊断)/SkyWalking(链路追踪)/Prometheus+Grafana(监控)。",
    "服务.*挂": "服务宕机处理：①健康检查(心跳检测,3次失败标记不健康) ②自动摘除(注册中心自动剔除不健康实例) ③重试(Retry+负载均衡切到其他实例) ④熔断(连续失败→快速失败,不再调用) ⑤降级(返回兜底数据) ⑥告警(通知运维) ⑦自动恢复(服务重启后自动注册)。Nacos：临时实例15s未心跳→不健康,30s→剔除。",
    "热.*数据.*过期": "热点数据缓存过期导致DB压力：①永不过期+异步更新(后台定时刷新) ②逻辑过期(在value中存过期时间,发现过期→异步更新+先返回旧值) ③互斥锁(SETNX只允许一个线程重建) ④多级缓存(本地缓存Caffeine+Redis) ⑤随机过期时间(防止同时失效)。核心：热点数据不应该同时过期。",
    "订单": "订单模块核心表：①订单主表(order_id/user_id/status/total_amount/create_time) ②订单明细表(order_id/product_id/quantity/price) ③支付记录表(order_id/pay_type/pay_time/transaction_id) ④物流表(order_id/express_no/status)。状态机：待支付→已支付→已发货→已完成/已取消/已退款。索引：user_id+status+create_time联合索引。",
    "问卷": "问卷系统表设计：①问卷表(questionnaire_id/title/description/status/create_time) ②题目表(question_id/questionnaire_id/type/content/options) type=单选/多选/填空/评分 ③回答表(answer_id/questionnaire_id/user_id/create_time) ④回答明细表(answer_id/question_id/option_id/content)。统计：GROUP BY+COUNT聚合。",

    # 面试软技能
    "专业课": "回答策略：列出与岗位相关的核心课程(数据结构/操作系统/计算机网络/数据库/设计模式),突出与Java后端相关的(面向对象/JVM/并发编程)。如果有项目经验,关联课程知识(如\"数据库课上学的范式在项目表设计中用到了\")。避免：说太多无关课程。",
    "学过什么": "回答策略：①核心技术栈(Java/Spring/MySQL/Redis) ②框架经验(SpringBoot/SpringCloud/MyBatis) ③中间件(MQ/ES/Docker) ④工具(Git/Maven/Linux) ⑤持续学习(最近在学什么)。关联岗位要求,突出匹配的技术。",
    "前端.*经验": "回答策略：①了解程度(能读懂/能简单修改/独立开发) ②具体技术(Vue/React/HTML/CSS/JS) ③实际项目(如果有前端经验) ④学习意愿。诚实回答,不要夸大。后端岗位前端能力是加分项但不是必须。",
    "场景": "场景题回答框架：①理解场景(确认需求和约束) ②分析方案(列出可能的方案) ③对比选型(各方案优缺点) ④最终选择(给出推荐方案和理由) ⑤补充(边界条件/扩展性/容错)。面试官看的是思考过程,不只是答案。",
    "画像": "用户画像：收集用户特征数据(基本属性/行为数据/偏好)→标签化→存储→应用(推荐/营销/风控)。存储：MySQL(结构化标签)/Redis(实时特征)/ES(检索)/HDFS(离线分析)。实时画像：Kafka+Flink流处理。离线画像：Hive+Spark批处理。",
    "在线.*系统": "系统设计题回答框架：①需求分析(功能/非功能需求) ②容量估算(QPS/存储/带宽) ③架构设计(分层:接入层/业务层/数据层) ④核心流程(时序图) ⑤数据设计(表结构/索引/分库分表) ⑥扩展性(缓存/消息队列/读写分离) ⑦可用性(主从/多活/容灾)。",

    # 通用技术
    "通用": "Java后端面试高频考点：①集合(ArrayList/HashMap/ConcurrentHashMap) ②并发(线程池/synchronized/volatile/CAS) ③JVM(内存模型/GC/调优) ④Spring(IOC/AOP/事务/Boot自动配置) ⑤MySQL(索引/事务/锁/优化) ⑥Redis(数据类型/缓存问题/分布式锁) ⑦MQ(Kafka/RabbitMQ) ⑧微服务(Nacos/Gateway/Feign)。建议：理解原理>背答案,结合项目经验回答。",
}

# Apply to "其他" category
patterns = []
for kw, answer in tech_answers.items():
    try:
        pat = re.compile(kw, re.IGNORECASE)
        patterns.append((pat, len(kw), answer))
    except:
        patterns.append((re.compile(re.escape(kw), re.IGNORECASE), len(kw), answer))
patterns.sort(key=lambda x: -x[1])

updated = 0
for q in data:
    if q['category'] != '其他':
        continue
    # Skip if already has a real answer (not the generic one)
    if q['answer'] and '建议结合项目经验' not in q['answer'] and len(q['answer']) > 80:
        continue
    
    question = q['question']
    best = None
    best_score = 0
    for pat, score, answer in patterns:
        if pat.search(question) and score > best_score:
            best_score = score
            best = answer
    
    if best:
        q['answer'] = best
        updated += 1
    else:
        # Keep the generic fallback for truly non-technical questions
        pass

with open('public/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Updated {updated} '其他' questions with technical answers")

# Final stats
from collections import Counter
good = sum(1 for q in data if q['answer'] and len(q['answer']) > 100)
bad = sum(1 for q in data if '建议结合项目经验' in q.get('answer', ''))
print(f"Good (>100 chars): {good} ({good*100//len(data)}%)")
print(f"Still generic: {bad} ({bad*100//len(data)}%)")
