import json, re

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# === 宽匹配答案库：关键词→答案 ===
# 之前的精确匹配覆盖不够，这里用更宽的模式
broad_answers = {
    # Java基础 - 宽匹配
    "集合": "Java集合框架：List(有序可重复,ArrayList/LinkedList)、Set(无序不重复,HashSet/TreeSet)、Queue(队列,LinkedList/PriorityQueue)、Map(键值对,HashMap/TreeMap/ConcurrentHashMap)。ArrayList底层动态数组(查询O(1),增删O(n))，LinkedList底层双向链表(查询O(n),增删O(1))。HashMap：数组+链表+红黑树(JDK8)，默认容量16，负载因子0.75。",
    "线程安全": "线程安全的集合：①Vector/Hashtable(古老,方法级synchronized,不推荐) ②Collections.synchronizedXxx()(包装类) ③CopyOnWriteArrayList(写时复制,读多写少) ④ConcurrentHashMap(分段锁/CAS,推荐) ⑤ConcurrentLinkedQueue(无锁队列)。HashMap线程不安全：多线程put可能导致数据丢失或链表成环(JDK7头插法)。",
    "sleep": "sleep()和wait()区别：①sleep是Thread静态方法,wait是Object方法 ②sleep不释放锁,wait释放锁 ③sleep到时间自动恢复,wait需要notify唤醒 ④sleep可在任何地方调用,wait必须在synchronized块内。",
    "线程池": "ThreadPoolExecutor 7参数：corePoolSize(核心线程数)、maximumPoolSize(最大线程数)、keepAliveTime(空闲存活时间)、unit(时间单位)、workQueue(任务队列)、threadFactory(线程工厂)、handler(拒绝策略:AbortPolicy/CallerRunsPolicy/DiscardPolicy/DiscardOldestPolicy)。流程：核心线程未满→创建核心线程；满了→放队列；队列满→创建非核心线程；都满→拒绝。",
    "线程状态": "6种状态：NEW(新建未start)、RUNNABLE(可运行/运行中)、BLOCKED(等待锁)、WAITING(无限等待:wait/join)、TIMED_WAITING(超时等待:sleep/wait(timeout))、TERMINATED(终止)。",
    "创建线程": "4种方式：①继承Thread ②实现Runnable ③实现Callable(有返回值,配合FutureTask) ④线程池ExecutorService。推荐线程池。",
    "volatile": "保证可见性(修改后立即刷新到主内存)和有序性(禁止指令重排),不保证原子性。底层通过内存屏障实现。典型应用：双重检查锁定的单例模式。",
    "synchronized": "内置互斥锁。修饰实例方法→锁this,修饰静态方法→锁Class对象,修饰代码块→锁指定对象。JDK6优化：偏向锁→轻量级锁(CAS)→重量级锁。",
    "反射": "运行时获取类信息并操作。获取Class：Class.forName()/类名.class/对象.getClass()。核心：Constructor/Method/Field。应用：Spring IOC/动态代理/注解处理。",
    "泛型": "编译时类型安全检查,避免强制转换。类型擦除后为Object。通配符：? extends T(上界,只读)、? super T(下界,只写)。PECS原则。",
    "String": "String是final类,不可变(每次修改创建新对象)。StringBuffer可变线程安全(synchronized),StringBuilder可变非线程安全。性能：StringBuilder > StringBuffer。循环拼接必须用StringBuilder。",
    "final": "修饰类→不可继承(String),修饰方法→不可重写,修饰变量→引用不可变(基本类型值不变,引用类型内容可变)。",
    "异常": "体系：Throwable→Error(不可恢复:OOM/SOF)/Exception→RuntimeException(运行时,不强制catch)/CheckedException(编译时,必须catch或throws)。常见：NullPointerException/ClassCastException/IndexOutOfBoundsException/IOException。",
    "IO": "BIO(同步阻塞,一个连接一个线程)→NIO(同步非阻塞,Channel+Buffer+Selector,多路复用)→AIO(异步非阻塞,回调通知)。NIO适用高并发连接,AIO适用大量长连接。",
    "代理": "静态代理(编译时,实现同一接口)。动态代理：JDK Proxy(基于接口,Proxy.newProxyInstance+InvocationHandler)和CGLIB(基于继承,生成子类字节码,无需接口)。Spring AOP默认：有接口用JDK,无接口用CGLIB(Spring Boot默认全用CGLIB)。",
    "内部类": "①成员内部类(非static,可访问外部类所有成员) ②静态内部类(static,只能访问外部类静态成员) ③局部内部类(方法内定义) ④匿名内部类(没有名字,常用于接口实现)。Lambda是函数式接口的简写,不是匿名内部类但效果类似。",
    "接口": "接口(Interface)：抽象方法的集合,类可以实现多个接口(JDK8后可有default方法)。抽象类(Abstract)：可以有具体方法和状态,类只能继承一个。选择：\"能做什么\"用接口,\"是什么\"用抽象类。接口支持多继承,抽象类支持状态。",
    "装箱": "自动装箱(Autoboxing)：基本类型→包装类(int→Integer),编译为Integer.valueOf()。自动拆箱(Unboxing)：包装类→基本类型,编译为intValue()。注意：Integer缓存-128~127,超出范围==比较返回false。null拆箱会NPE。",
    "多态": "同一个方法调用,根据对象实际类型执行不同的实现。条件：①继承/实现关系 ②方法重写 ③父类引用指向子类对象。实现机制：方法表+动态绑定(运行时根据实际类型查找方法)。好处：代码灵活可扩展(面向接口编程)。",
    "继承": "子类继承父类的属性和方法。Java单继承(一个类只能extends一个父类),但可以实现多个接口。子类构造器默认调用父类无参构造器(super())。不能继承：private成员/构造器/final类。方法重写(Override)：子类覆盖父类方法,访问权限不能缩小,异常不能扩大。",

    # Spring 宽匹配
    "Spring.*IOC": "IOC(控制反转)：对象创建和依赖管理交给Spring容器。DI(依赖注入)是实现方式：构造器注入(推荐)/Setter注入/字段注入(@Autowired)。好处：解耦/便于测试/统一管理生命周期。",
    "Spring.*AOP": "AOP(面向切面编程)：将日志/事务/权限等横切关注点从业务逻辑中分离。核心：切面(Aspect)+切点(Pointcut)+通知(Advice:Before/After/Around)。底层：JDK动态代理(接口)/CGLIB(类)。",
    "Spring.*注解": "核心注解：@Component(组件)/@Service(服务)/@Repository(数据层)/@Controller(控制器)/@Autowired(注入)/@Qualifier(指定名称)/@Scope(作用域)/@Configuration(配置类)/@Bean(注册Bean)/@Value(注入配置)/@Transactional(事务)/@Aspect(切面)/@Scheduled(定时任务)。",
    "Spring.*事务": "@Transactional。属性：propagation(传播行为,默认REQUIRED)/isolation(隔离级别)/rollbackFor(回滚异常)。传播行为：REQUIRED(有就加入)/REQUIRES_NEW(总是新建)/NESTED(嵌套)。坑：同类方法调用不走代理事务失效/checked异常不回滚需指定rollbackFor。",
    "Spring.*设计模式": "①工厂(BeanFactory) ②单例(Bean默认singleton) ③代理(AOP) ④模板(JdbcTemplate) ⑤观察者(ApplicationEvent) ⑥适配器(HandlerAdapter) ⑦策略(Resource/InstantiationStrategy)。",

    # SpringBoot 宽匹配
    "SpringBoot.*自动装配": "@SpringBootApplication=@SpringBootConfiguration+@EnableAutoConfiguration+@ComponentScan。原理：@EnableAutoConfiguration→加载META-INF/spring.factories→@Conditional条件装配→满足条件则生效。",
    "SpringBoot.*自动配置": "@SpringBootApplication=@SpringBootConfiguration+@EnableAutoConfiguration+@ComponentScan。原理：@EnableAutoConfiguration→加载META-INF/spring.factories→@Conditional条件装配→满足条件则生效。",
    "SpringBoot.*好处": "①约定优于配置,减少XML ②内嵌Tomcat,jar直接运行 ③自动配置+starter ④Actuator监控 ⑤外部化配置(yml)。本质：Spring的脚手架,简化搭建和开发。",
    "SpringBoot.*区别.*Spring": "SpringBoot是Spring的快速开发脚手架。区别：①Spring需要大量XML配置,Boot通过自动配置+starter减少 ②Boot内嵌Tomcat直接运行 ③Boot提供Actuator监控。Boot不是替代Spring,是简化Spring。",
    "SpringBoot.*区别.*SpringCloud": "SpringBoot：单个微服务的快速开发框架。SpringCloud：微服务架构的解决方案(注册中心/网关/配置中心/熔断等)。关系：SpringCloud基于SpringBoot构建。Boot关注单服务开发,Cloud关注服务间协作。",

    # SpringCloud 宽匹配
    "注册中心": "服务注册与发现。服务启动时注册到注册中心,其他服务通过注册中心发现可用实例。主流：Nacos(推荐,支持AP/CP切换)/Eureka(AP,自我保护)/Consul(CP)/Zookeeper(CP)。心跳续约：服务定期发送心跳,超时则剔除。",
    "网关": "API网关：统一入口,路由转发/负载均衡/限流/鉴权/日志。Spring Cloud Gateway(推荐,基于WebFlux非阻塞)：Route(路由)+Predicate(断言)+Filter(过滤器)。比Zuul性能更好。",
    "远程调用": "微服务间HTTP调用。Feign：声明式客户端(@FeignClient定义接口,像调本地方法)。底层：动态代理→构造HTTP→Ribbon负载均衡→发送。集成Sentinel做熔断降级。",
    "熔断降级": "熔断：服务调用失败率达阈值→自动切断(返回降级结果),防止故障蔓延。三状态：CLOSED→OPEN(熔断)→HALF-OPEN(试探)。降级：返回兜底数据/默认值。Sentinel：@SentinelResource注解配置。",
    "分布式事务": "跨服务的事务一致性。方案：①2PC(强一致但慢) ②TCC(业务侵入大) ③本地消息表(最终一致) ④Seata(推荐,AT模式自动补偿)。Seata AT：一阶段提交本地事务+写undo log,二阶段提交删undo log/回滚用undo log反向补偿。",

    # MySQL 宽匹配
    "索引": "B+树索引(默认)。特点：非叶子节点只存key,叶子节点存数据且双向链表连接。优势：范围查询快,IO少(3-4层可索引千万数据)。类型：主键索引/唯一索引/普通索引/联合索引/全文索引。联合索引遵循最左匹配原则。",
    "事务": "ACID：原子性(undo log)/一致性(AID共同保证)/隔离性(MVCC+锁)/持久性(redo log)。隔离级别：读未提交(脏读)/读已提交(不可重复读)/可重复读(MySQL默认,InnoDB通过MVCC+间隙锁解决幻读)/串行化。",
    "优化": "SQL优化：①避免SELECT * ②合理建索引用EXPLAIN验证 ③WHERE中避免函数运算 ④小表驱动大表 ⑤LIMIT深分页用id>offset ⑥批量INSERT ⑦开启慢查询日志。EXPLAIN关键：type(访问类型)/key(使用索引)/rows(扫描行数)/Extra(Using index/filesort/temporary)。",
    "锁": "InnoDB锁：①共享锁(S锁,SELECT...LOCK IN SHARE MODE)/排他锁(X锁,SELECT...FOR UPDATE) ②行锁(索引命中时)/表锁(未命中索引时退化为表锁) ③间隙锁(Gap Lock,防止幻读) ④临键锁(Next-Key Lock=行锁+间隙锁)。乐观锁(版本号CAS)/悲观锁(FOR UPDATE)。",
    "MVCC": "Multi-Version Concurrency Control,多版本并发控制。每行数据有隐藏字段：trx_id(最后修改的事务ID)+roll_pointer(指向undo log旧版本)。ReadView：记录当前活跃事务列表,根据可见性规则判断哪个版本对当前事务可见。RC级别每次SELECT生成新ReadView,RR级别只在第一次SELECT生成。",
    "主从": "主从复制：Master写入→binlog→Slave的IO线程拉取→relay log→SQL线程执行。读写分离：写操作走Master,读操作走Slave(ProxySQL/MyCat中间件或应用层路由)。延迟问题：异步复制有延迟,半同步复制至少一个Slave确认收到。",

    # Redis 宽匹配
    "Redis": "内存数据库,支持String/List/Hash/Set/ZSet等数据结构。用途：缓存/分布式锁/排行榜/计数器/消息队列/Session共享。持久化：RDB(快照)/AOF(追加命令)/混合。集群：Sentinel(哨兵,高可用)/Cluster(分片,水平扩展)。",
    "缓存": "缓存三大问题：①雪崩(大量key同时过期→随机过期时间/多级缓存) ②击穿(热点key过期→互斥锁/逻辑过期) ③穿透(查询不存在的数据→布隆过滤器/缓存空值)。缓存一致性：先更新DB→再删缓存+延迟双删/Canal监听binlog。",
    "分布式锁": "Redis实现：SET key uuid NX EX 30(原子操作)。释放：Lua脚本(先比较value再DEL)。Redisson：看门狗自动续期/可重入锁/RedLock(多节点)。问题：主从切换可能丢锁→RedLock解决。",

    # JVM 宽匹配
    "JVM": "内存：堆(对象,GC主战场)/方法区(类信息)/虚拟机栈(栈帧)/本地方法栈/程序计数器。GC算法：标记-清除/标记-复制/标记-整理/分代收集。收集器：G1(JDK9默认)/ZGC(超低延迟)。调优：-Xms/-Xmx/-Xmn/-XX:+UseG1GC。",
    "垃圾回收": "GC Roots可达性分析。GC Roots：栈帧局部变量/静态变量/常量/同步锁持有对象。不可达即为垃圾。算法：标记-清除(碎片)/标记-复制(浪费空间)/标记-整理(慢但无碎片)。分代：新生代(Eden+Survivor,复制算法)/老年代(标记整理)。",
    "OOM": "①Java Heap Space(对象太多,-Xmx) ②Metaspace(动态类太多,-XX:MaxMetaspaceSize) ③GC Overhead(GC时间>98%但回收<2%) ④Direct Buffer Memory(NIO) ⑤StackOverflowError(递归太深,-Xss)。",
    "类加载": "加载→验证→准备→解析→初始化。双亲委派：收到请求→先委托父加载器→找不到→自己加载。好处：避免重复加载/安全(防覆盖核心类)。打破：重写loadClass()/线程上下文类加载器(SPI)。",

    # 消息队列 宽匹配
    "Kafka": "分布式流平台。核心：Topic(主题)/Partition(分区,有序)/Offset(位移)/Broker(服务器)/ConsumerGroup(消费者组,组内竞争)。消息不丢失：producer(acks=all)/broker(replication≥3)/consumer(手动提交offset)。顺序：同一Partition内有序。",
    "消息队列": "MQ作用：①异步处理 ②流量削峰 ③系统解耦。选型：Kafka(高吞吐,日志/流处理)/RabbitMQ(低延迟,业务消息)/RocketMQ(事务消息)。消息不丢失：producer确认+broker持久化+consumer手动ACK。幂等：消息ID去重。",
    "消息丢失": "①Producer：同步发送+重试 ②Broker：acks=all+多副本 ③Consumer：手动提交offset。RabbitMQ：持久化+confirm+手动ACK。",

    # MyBatis 宽匹配
    "MyBatis": "ORM框架,将SQL映射为Java方法。核心：Mapper接口+XML/注解SQL。#{}预编译防注入,${}字符串拼接(有注入风险)。resultType自动映射,resultMap手动映射。动态SQL：if/choose/where/set/foreach。一级缓存SqlSession级别,二级缓存Mapper级别。",
    "mybatis": "ORM框架,将SQL映射为Java方法。核心：Mapper接口+XML/注解SQL。#{}预编译防注入,${}字符串拼接(有注入风险)。resultType自动映射,resultMap手动映射。动态SQL：if/choose/where/set/foreach。一级缓存SqlSession级别,二级缓存Mapper级别。",
    "mybatis-plus": "MyBatis增强工具。BaseMapper提供CRUD接口(单表零SQL)。内置分页插件/代码生成器/逻辑删除/自动填充/乐观锁。Wrapper条件构造器(链式调用)。简单CRUD用MP,复杂SQL手写XML。",

    # Docker/DevOps 宽匹配
    "Docker": "容器化平台。镜像(Image,只读模板)/容器(Container,运行实例)/仓库(Registry)。Dockerfile：FROM/RUN/COPY/ADD/CMD/EXPOSE/ENTRYPOINT。常用：docker run/build/ps/logs/exec/stop。镜像分层共享基础层。",
    "Linux": "常用命令：ls/cd/cp/mv/rm/mkdir/cat/grep/find/chmod/ps/top/netstat/df/free/tar/curl/vim。部署：systemctl启停服务,nginx配置,tomcat部署。",
    "nginx": "反向代理+负载均衡+静态资源服务。配置：server块(虚拟主机)/location块(路由)/proxy_pass(转发)。负载均衡：轮询/权重/ip_hash/least_conn。热重载：nginx -s reload。",
    "Jenkins": "CI/CD工具。流程：代码提交→自动构建→自动测试→自动部署。Pipeline：Jenkinsfile定义构建流水线。与Git集成：Webhook触发自动构建。",

    # 设计模式 宽匹配
    "单例": "一个类只有一个实例。实现：①饿汉式(类加载时创建) ②懒汉式(synchronized) ③双重检查锁(volatile+synchronized) ④静态内部类(推荐) ⑤枚举(最安全,Effective Java推荐)。Spring Bean默认单例。",
    "工厂": "创建对象不暴露创建逻辑。简单工厂(一个工厂类根据参数创建)/工厂方法(每个产品一个工厂)/抽象工厂(创建产品族)。Spring BeanFactory是工厂模式。",
    "代理": "为其他对象提供代理以控制访问。静态代理(编译时)/动态代理(JDK基于接口/CGLIB基于继承)。Spring AOP核心机制。",

    # ES 宽匹配
    "Elasticsearch": "基于Lucene的分布式全文搜索引擎。倒排索引：文档→分词→\"词项→文档ID列表\"映射。核心概念：Index(索引)/Document(文档)/Field(字段)/Shard(分片)/Replica(副本)。与MySQL同步：Canal监听binlog(推荐)/双写/MQ异步。",
    "ES": "基于Lucene的分布式全文搜索引擎。倒排索引：文档→分词→\"词项→文档ID列表\"映射。核心概念：Index(索引)/Document(文档)/Field(字段)/Shard(分片)/Replica(副本)。与MySQL同步：Canal监听binlog(推荐)/双写/MQ异步。",

    # 分布式 宽匹配
    "分布式锁": "实现：①Redis(SET NX EX,Redisson生产级) ②Zookeeper(临时顺序节点+Watch,Curator) ③数据库(唯一索引)。Redisson：看门狗续期/可重入/RedLock。选型：性能优先→Redis,可靠性优先→Zookeeper。",
    "分布式事务": "CAP定理(一致性/可用性/分区容错不可兼得)。方案：2PC(强一致)/TCC(补偿)/本地消息表(最终一致)/Seata(推荐,AT模式自动补偿)。Seata AT：一阶段提交+undo log,二阶段提交删log/回滚用log反向补偿。",
    "CAP": "分布式系统三要素：Consistency(一致性)/Availability(可用性)/Partition tolerance(分区容错)。最多同时满足两个。CP：Zookeeper(一致性优先)。AP：Eureka(可用性优先)。实际：分区容错必选,所以是CP或AP。",

    # MongoDB 宽匹配
    "MongoDB": "文档型NoSQL数据库。BSON(Binary JSON)格式存储。特点：灵活Schema/水平扩展(分片)/高性能读写。适用：内容管理/日志/实时分析。与MySQL对比：弱事务/灵活查询/易扩展。MongoDB 4.0+支持多文档ACID事务。",

    # 项目与场景 宽匹配
    "登录": "典型流程：①前端提交用户名+密码 ②后端BCrypt加密比较 ③校验通过生成JWT Token ④前端存储Token ⑤后续请求携带Token(Authorization: Bearer xxx) ⑥拦截器校验Token。JWT组成：Header.Payload.Signature。过期处理：Refresh Token机制。",
    "JWT": "JSON Web Token。三部分：Header(算法)+Payload(数据)+Signature(签名)。特点：无状态/可扩展/跨域。vs Session：JWT存客户端不占服务端内存,但无法主动失效。过期：短access token(2h)+长refresh token(7d)。",
    "单点登录": "一次登录,所有系统共享。CAS流程：访问A→未登录→重定向SSO→登录→带Ticket回A→A向SSO验证→创建本地会话。访问B→B重定向SSO→已登录→给Ticket→B验证→创建本地会话。",
    "高并发": "①缓存(Redis) ②异步(MQ削峰) ③限流(令牌桶/滑动窗口) ④降级(兜底数据) ⑤熔断(快速失败) ⑥负载均衡(Nginx) ⑦读写分离 ⑧CDN ⑨池化(线程池/连接池) ⑩集群。",
    "SQL优化": "①避免SELECT * ②合理索引(EXPLAIN验证) ③WHERE避免函数运算 ④小表驱动大表 ⑤LIMIT深分页优化 ⑥批量INSERT ⑦慢查询日志定位。",
    "项目介绍": "回答框架：①项目背景(解决什么问题) ②技术架构(SpringCloud/MySQL/Redis/ES) ③我负责的模块(具体功能) ④技术难点和解决方案 ⑤成果(性能指标/业务指标)。避免：说太多无关细节/夸大贡献。",

    # HR 宽匹配
    "自我介绍": "模板：面试官好,我是XXX,XX学校XX专业。上家公司负责XX项目,使用XX技术栈,独立完成XX模块。对贵公司XX岗位很感兴趣。控制在1-2分钟,突出与岗位相关的技术栈和项目经验。",
    "离职原因": "正面表述：①寻求更大发展空间 ②技术方向调整 ③业务调整。避免：钱少/加班多/领导不行。",
    "职业规划": "短期(1-2年)：深入核心技术,独立负责核心模块。中期(3-5年)：技术骨干或架构师。长期：技术管理或资深架构。结合应聘岗位说。",
    "薪资": "回答策略：①先了解市场行情 ②给出范围而非具体数字 ③强调看重发展机会 ④如果被追问,说\"根据岗位和职责,期望XX-XX\"。避免：报太高吓跑/报太低吃亏。",
}

# Compile patterns
patterns = []
for keyword, answer in broad_answers.items():
    try:
        pat = re.compile(keyword, re.IGNORECASE)
        patterns.append((pat, len(keyword), answer))
    except:
        patterns.append((re.compile(re.escape(keyword), re.IGNORECASE), len(keyword), answer))

# Sort by keyword length (longer = more specific = higher priority)
patterns.sort(key=lambda x: -x[1])

def find_answer(question):
    q = question
    best = None
    best_score = 0
    for pat, score, answer in patterns:
        if pat.search(q) and score > best_score:
            best_score = score
            best = answer
    return best

# Apply
updated = 0
for q in data:
    a = q['answer']
    # Only replace bad answers
    if not a or len(a) < 20 or '暂无标准答案' in a or '这是一道' in a or '通用参考' in a or '结合自己项目' in a:
        new_a = find_answer(q['question'])
        if new_a:
            q['answer'] = new_a
            updated += 1

with open('public/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Updated {updated} bad answers")

# Re-check
good = sum(1 for q in data if q['answer'] and len(q['answer']) > 100 and '这是一道' not in q['answer'] and '暂无' not in q['answer'])
bad = sum(1 for q in data if not q['answer'] or len(q['answer']) < 20 or '暂无' in q['answer'] or '这是一道' in q['answer'])
print(f"Good: {good} ({good*100//len(data)}%)")
print(f"Bad: {bad} ({bad*100//len(data)}%)")
