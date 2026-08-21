import json

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Replace generic "建议结合项目经验" with category-specific technical summaries
category_tech = {
    "其他": "此题属于项目经验/场景题。回答框架：①明确需求(确认场景和约束) ②技术选型(为什么用这个方案) ③核心实现(关键代码/难点) ④优化(做了哪些优化) ⑤成果(量化指标)。技术面重点：展现你的技术深度和独立思考能力,不要只说\"做了什么\",要说\"为什么这么做\"和\"遇到了什么问题,怎么解决的\"。",
    "项目与场景": "项目经验题。回答建议用STAR法则：①Situation(项目背景) ②Task(你的职责) ③Action(技术方案和实现) ④Result(成果和数据)。选择有技术深度的例子,重点讲难点和解决方案。避免泛泛而谈,要具体到技术细节(如\"用Redis缓存热点数据,缓存击穿用互斥锁解决\")。",
    "Spring": "Spring核心：IOC容器管理Bean生命周期和依赖注入(DI)。AOP面向切面编程(日志/事务/权限,底层JDK动态代理或CGLIB)。Bean默认单例,支持singleton/prototype/request/session。事务@Transactional(传播行为/隔离级别/rollbackFor)。SpringBoot自动配置(spring.factories+@Conditional)。",
    "MySQL": "MySQL核心：InnoDB引擎(B+树索引/MVCC无锁读/行锁+间隙锁)。事务ACID(原子性undo log/一致性/隔离性MVCC+锁/持久性redo log)。索引优化(EXPLAIN/type/key/rows/Extra)。慢查询日志定位+SQL优化(避免SELECT */合理索引/小表驱动大表)。主从复制(binlog→relay log→重放)。",
    "多线程与并发": "Java并发核心：线程池7参数+拒绝策略。synchronized(偏向→轻量→重量锁升级)vs ReentrantLock(可中断/公平锁)。volatile(可见性+有序性)。CAS(无锁并发,ABA问题用AtomicStampedReference)。AQS(抽象队列同步器,ReentrantLock/Semaphore/CountDownLatch底层)。ConcurrentHashMap(JDK8:CAS+synchronized)。",
    "Redis": "Redis核心：5种基本类型(String/List/Hash/Set/ZSet)。持久化(RDB快照/AOF追加/混合)。缓存问题(雪崩→随机过期/击穿→互斥锁/穿透→布隆过滤器)。分布式锁(SET NX EX+Lua释放,Redisson看门狗续期)。集群(Sentinel哨兵高可用/Cluster分片扩展)。过期策略(惰性删除+定期删除)。",
    "JVM": "JVM核心：内存(堆分新生代Eden+Survivor和老年代/方法区/虚拟机栈/程序计数器)。GC(标记-复制新生代/标记-整理老年代)。收集器(G1分Region/ZGC超低延迟)。调优(-Xms/-Xmx/-XX:+UseG1GC/-XX:MaxGCPauseMillis)。OOM排查(Heap Space/Metaspace/StackOverflow)。双亲委派(Bootstrap→Extension→Application)。",
    "集合框架": "Java集合：ArrayList(数组,查询O(1))vs LinkedList(链表,增删O(1))。HashMap(数组+链表+红黑树,默认16/负载0.75/扩容2倍)。ConcurrentHashMap(JDK8:CAS+synchronized锁桶)。HashSet(HashMap的key)。TreeMap(红黑树,有序)。Queue/Deque(ArrayDeque/LinkedList/PriorityQueue)。",
    "SpringCloud": "微服务组件：Nacos(注册中心+配置中心,AP/CP切换)。Gateway(网关,路由+断言+过滤器,WebFlux非阻塞)。Feign(声明式HTTP客户端,集成Ribbon负载均衡)。Sentinel(熔断降级)。Seata(分布式事务,AT模式自动补偿)。OpenFeign+负载均衡+熔断=服务间可靠调用。",
    "Docker与DevOps": "Docker(镜像/容器/仓库,Dockerfile FROM/RUN/COPY/CMD)。CI/CD(Jenkins Pipeline自动构建测试部署)。Linux(ps/top/netstat/df/free/grep)。Nginx(反向代理/负载均衡/静态资源)。K8s(Pod/Service/Deployment容器编排)。Git(branch/merge/rebase分支管理)。Maven(compile/test/package/install/deploy生命周期)。",
    "Java基础": "Java核心：8种基本类型。面向对象(封装/继承/多态/抽象)。String不可变(final char[])。异常(Error/RuntimeException/CheckedException)。IO(BIO/NIO/AIO)。反射(运行时获取类信息)。泛型(编译时类型安全,类型擦除)。Lambda(函数式接口)。Stream(流式API)。JDK8新特性(接口default方法/Optional/日期API)。",
    "消息队列": "MQ核心：异步+削峰+解耦。Kafka(高吞吐,Partition有序,acks=all防丢失,ConsumerGroup)。RabbitMQ(低延迟,Exchange路由,Durable持久化)。消息不丢失(Producer确认+Broker持久化+Consumer手动ACK)。幂等(消息ID去重)。顺序(同Partition/同Queue)。积压(扩容消费者/优化消费逻辑)。",
    "Elasticsearch": "ES核心：倒排索引(分词→词项→文档ID列表)。Index/Document/Field/Shard/Replica。DSL查询(match分词/term精确/bool组合/must+should+filter)。与MySQL同步(Canal监听binlog/双写/MQ)。分词器(IK中文分词)。高亮/聚合/分页。性能优化(合理分词/路由/过滤代替查询)。",
    "分布式": "分布式核心：CAP定理(C/A/P不可兼得)。分布式事务(2PC/TCC/Seata AT)。分布式锁(Redis SETNX/Zookeeper临时节点)。分布式ID(雪花算法/UUID/Redis自增)。一致性哈希(数据分片)。Raft共识(Leader选举/日志复制)。微服务拆分(按业务领域/单一职责)。",
    "设计模式": "常用：①单例(5种实现,枚举最安全) ②工厂(创建对象不暴露逻辑) ③代理(动态代理,AOP基础) ④策略(算法可替换) ⑤模板方法(骨架+子类) ⑥观察者(事件通知) ⑦适配器(接口转换)。Spring中：工厂(BeanFactory)/单例(Bean)/代理(AOP)/模板(JdbcTemplate)/观察者(ApplicationEvent)。",
    "MyBatis": "MyBatis：Mapper接口+XML/注解SQL。#{}预编译防注入,${}字符串拼接。resultType自动映射,resultMap手动映射。动态SQL(if/choose/where/set/foreach/trim)。一级缓存SqlSession,二级缓存Mapper。MyBatis-Plus：BaseMapper CRUD+分页插件+代码生成器+逻辑删除+自动填充。",
    "MongoDB与NoSQL": "MongoDB文档型NoSQL,BSON格式。灵活Schema/水平扩展(分片)/高性能。CRUD：insert/find/update/delete。索引(单字段/复合/文本/地理空间)。聚合管道(match→group→sort→project)。vs MySQL：弱事务/灵活查询/易扩展。适用：内容管理/日志/实时分析/物联网。",
    "HR与软技能": "HR面试：①自我介绍(1-2分钟,技术栈+项目亮点) ②离职原因(正面表述) ③职业规划(短期深入技术/中期技术骨干) ④薪资(给范围,了解行情) ⑤优缺点(缺点说正在改进的)。关键：自信诚实,与岗位匹配,用具体事例支撑(如\"我在XX项目中独立解决了XX问题\")。",
    "SpringBoot": "SpringBoot：@SpringBootApplication自动配置(spring.factories+@Conditional)。starter依赖自动引入。内嵌Tomcat jar直接运行。Actuator监控。yml配置(多环境profile)。与Spring的关系：Boot是Spring的脚手架,简化配置和部署。",
    "LLM大模型": "大模型技术：Transformer(Self-Attention+FFN)。训练(预训练→SFT→RLHF/DPO)。推理优化(KV Cache/Flash Attention/量化/推测解码)。应用(Prompt Engineering/RAG/Function Calling/Agent)。模型(GPT-4/Claude/LLaMA/Qwen/DeepSeek)。评估(MMLU/HumanEval/Chatbot Arena)。",
    "AI Agent": "Agent核心：LLM+Tools+Memory+Planning。ReAct(推理+行动交替)。工具调用(Function Calling/MCP协议)。Multi-Agent(CrewAI/AutoGen/LangGraph)。记忆(短期上下文+长期向量库)。评估(SWE-bench/WebArena/AgentBench)。安全(沙箱执行/权限最小化/输入过滤)。",
}

updated = 0
for q in data:
    if '建议结合项目经验' not in q.get('answer', ''):
        continue
    cat = q['category']
    if cat in category_tech:
        q['answer'] = category_tech[cat]
        updated += 1

with open('public/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

good = sum(1 for q in data if q['answer'] and len(q['answer']) > 100)
bad = sum(1 for q in data if '建议结合项目经验' in q.get('answer', ''))
print(f"Updated: {updated}")
print(f"Good (>100 chars): {good} ({good*100//len(data)}%)")
print(f"Still generic: {bad}")
