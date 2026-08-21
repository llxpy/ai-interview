import json, re

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# === Comprehensive answer templates ===
# Key: keyword/phrase to match (lowercase)
# Value: answer text

detailed_answers = {
    # === Java基础 ===
    "基本数据类型": "Java有8种基本数据类型：byte(1字节,-128~127)、short(2字节)、int(4字节)、long(8字节)、float(4字节)、double(8字节)、char(2字节,Unicode)、boolean(JVM未明确规定大小)。String不是基本类型，是final修饰的不可变对象。",
    "包装类": "每个基本类型对应一个包装类：Byte、Short、Integer、Long、Float、Double、Character、Boolean。优势：可用于泛型、可为null、提供工具方法。自动装箱/拆箱是JDK5语法糖，编译后调用valueOf()/xxxValue()。Integer缓存-128~127。",
    "equals和==": "==比较引用地址（基本类型比较值），equals()比较内容。String重写了equals()按字符逐一比较。注意：Integer在-128~127范围内==返回true（IntegerCache），超出范围返回false（new了不同对象）。",
    "sleep和wait": "①sleep()是Thread静态方法，wait()是Object方法 ②sleep()不释放锁，wait()释放锁并进入等待队列 ③sleep()到时间自动恢复，wait()必须由notify()/notifyAll()唤醒 ④sleep()可在任何位置调用，wait()必须在synchronized块内 ⑤sleep()抛InterruptedException，wait()不抛",
    "线程状态": "6种状态：NEW(刚创建未start)、RUNNABLE(就绪/运行中)、BLOCKED(等待锁)、WAITING(无限等待,wait/join)、TIMED_WAITING(超时等待,sleep/wait(timeout))、TERMINATED(执行完毕)。getState()获取当前状态。",
    "创建线程": "4种方式：①继承Thread类重写run() ②实现Runnable接口 ③实现Callable接口(有返回值,配合FutureTask) ④线程池ExecutorService.submit()。推荐线程池，避免频繁创建销毁开销。Callable是唯一有返回值的方式。",
    "线程池参数": "ThreadPoolExecutor 7个参数：①corePoolSize核心线程数(即使空闲也不回收) ②maximumPoolSize最大线程数 ③keepAliveTime非核心线程空闲存活时间 ④unit时间单位 ⑤workQueue任务队列(ArrayBlockingQueue/LinkedBlockingQueue/SynchronousQueue) ⑥threadFactory线程工厂 ⑦handler拒绝策略(AbortPolicy抛异常/CallerRunsPolicy调用者执行/DiscardPolicy丢弃/DiscardOldestPolicy丢弃最早)",
    "线程池工作流程": "①提交任务→核心线程未满→创建核心线程执行 ②核心线程满→放入任务队列 ③队列满→创建非核心线程执行 ④非核心线程也满→触发拒绝策略。关键：核心线程在任务队列满之前就会创建，不是队列满了才创建。",
    "volatile": "保证可见性和有序性，不保证原子性。可见性：线程修改volatile变量后立即刷新到主内存，其他线程读取时从主内存取最新值。有序性：通过内存屏障禁止指令重排序。典型应用：双重检查锁定的单例模式中修饰instance变量。",
    "synchronized": "Java内置互斥锁。修饰实例方法→锁this对象 修饰静态方法→锁Class对象 修饰代码块→锁指定对象。JDK6优化：无锁→偏向锁→轻量级锁(CAS自旋)→重量级锁(阻塞)。底层：方法级用ACC_SYNCHRONIZED标志，代码块用monitorenter/monitorexit指令。",
    "死锁": "4个必要条件：①互斥(资源独占) ②占有且等待(持有资源并等待其他资源) ③不可抢占(不能强行夺取) ④循环等待(A等B,B等A)。避免方法：①按固定顺序获取锁 ②设置超时(tryLock) ③减少锁粒度 ④使用并发工具替代(synchronized→ReentrantLock)。",
    "ThreadLocal": "为每个线程提供独立变量副本，实现线程隔离。底层：每个Thread持有ThreadLocalMap，key是ThreadLocal的弱引用，value是实际值。注意内存泄漏：用完必须调remove()。典型应用：数据库连接、Session管理、日期格式化。在线程池中尤其要注意remove，否则线程复用会读到脏数据。",
    "反射": "运行时获取类信息并操作属性/方法。核心类：Class、Constructor、Method、Field。获取Class：①Class.forName(\"全类名\") ②类名.class ③对象.getClass() ④类加载器.loadClass()。应用：Spring IOC容器、动态代理、注解处理、序列化。性能开销较大，频繁调用应缓存。",
    "泛型": "编译时类型安全检查，避免强制转换。泛型类(如List<T>)、泛型接口(如Comparable<T>)、泛型方法(public <T> T method())。类型擦除：编译后泛型信息擦除为Object(上界通配符擦除为上界类型)。通配符：? extends T(上界,只读)、? super T(下界,只写)、?(无界)。PECS原则：Producer Extends, Consumer Super。",
    "String": "String是final类，底层final char[]（JDK9+改为byte[]），不可变。每次修改创建新对象。StringBuffer可变且线程安全(方法加synchronized)，StringBuilder可变且非线程安全。性能：StringBuilder > StringBuffer > String。字符串拼接用StringBuilder，循环拼接尤其注意。String.intern()将字符串放入常量池。",
    "final": "修饰类→不能被继承(如String、Integer) 修饰方法→不能被重写 修饰变量→引用不可变(基本类型值不变,引用类型引用不变但对象内容可变)。final变量必须在声明时或构造器中初始化。final参数不能被重新赋值。final提高安全性和编译器优化机会。",
    "反射.*用": "反射在项目中的常见应用：①Spring IOC通过反射创建Bean ②MyBatis通过反射将ResultSet映射为POJO ③JUnit通过反射调用测试方法 ④自定义注解+反射实现AOP ⑤JSON序列化/反序列化框架(Jackson/Gson)通过反射读写字段。代码示例：Class.forName(\"com.example.User\").getDeclaredConstructor().newInstance()",

    # === 集合框架 ===
    "ArrayList和LinkedList": "ArrayList底层Object[]动态数组，默认容量10，扩容1.5倍(Arrays.copyOf)，随机访问O(1)，尾部增删O(1)，中间增删O(n)需移动元素。LinkedList底层双向链表，随机访问O(n)需遍历，增删O(1)只需改指针。实际开发中ArrayList远优于LinkedList(CPU缓存友好)。",
    "HashMap原理": "JDK8：数组+链表+红黑树。默认容量16，负载因子0.75，扩容2倍。put流程：①计算hash(key.hashCode()高16位异或低16位) ②(容量-1)&hash定位桶 ③桶空直接放 ④桶非空比较key(先比hash再equals) ⑤相同覆盖 ⑥不同则链表尾插 ⑦链表长度≥8且数组≥64→转红黑树。线程不安全：多线程并发put可能导致数据丢失、链表成环(JDK7头插法)。",
    "ConcurrentHashMap": "JDK7：Segment分段锁(16段),不同段可并发。JDK8：CAS+synchronized锁桶头节点。put：桶空→CAS插入 非空→synchronized锁头节点→链表/红黑树插入。size()：通过counterCells分段计数求和(类似LongAdder)。不允许null key/value。读操作无锁(volatile修饰Node的val和next)。",
    "HashMap和HashTable": "①HashMap线程不安全,HashTable线程安全(方法级synchronized) ②HashMap允许null key和value,HashTable不允许 ③HashMap初始16扩容2倍,HashTable初始11扩容2n+1 ④HashMap效率远高于HashTable(锁粒度粗) ⑤多线程用ConcurrentHashMap替代HashTable",

    # === MySQL ===
    "索引原理": "MySQL默认使用B+树索引。B+树特点：①非叶子节点只存key不存数据(更多key→更矮→更少IO) ②叶子节点存所有数据且用双向链表连接(支持范围查询) ③树高度通常3-4层(千万级数据3次IO)。对比B树：B+树叶子节点形成有序链表,范围查询更高效。对比Hash索引：Hash只支持等值查询,不支持范围和排序。",
    "索引失效": "①对索引列使用函数或运算(如WHERE YEAR(create_time)=2024) ②隐式类型转换(如varchar列用int查询) ③以%开头的LIKE(如'%abc') ④OR连接(部分列无索引时全表扫描) ⑤违反最左匹配原则 ⑥NOT IN/NOT EXISTS/!=/<> ⑦IS NULL/IS NOT NULL(取决于数据分布和优化器判断)。用EXPLAIN的type列判断是否走索引。",
    "最左匹配原则": "联合索引(a,b,c)相当于创建了(a)、(a,b)、(a,b,c)三个索引。查询条件必须从最左列开始连续匹配。WHERE a=1 AND b=2→使用索引 WHERE b=2→不使用(跳过了a) WHERE a=1 AND c=3→只用到a(c不连续) WHERE b=2 AND c=3→不使用。优化器会自动调整WHERE条件顺序,所以WHERE b=2 AND a=1也能用索引。",
    "覆盖索引": "查询列全部在索引中,无需回表查数据行。如索引(name,age),SELECT name,age WHERE name='x'就是覆盖索引。EXPLAIN的Extra列显示Using index。优势：减少随机IO(不需要回表到聚簇索引)。实践：高频查询的字段建联合索引实现覆盖索引。",
    "事务隔离级别": "①READ UNCOMMITTED(读未提交)→脏读 ②READ COMMITTED(读已提交)→不可重复读(Oracle默认) ③REPEATABLE READ(可重复读,MySQL InnoDB默认)→幻读(InnoDB通过MVCC+间隙锁解决) ④SERIALIZABLE(串行化)→最安全最慢。MySQL查看：SELECT @@transaction_isolation 设置：SET TRANSACTION ISOLATION LEVEL ...",
    "ACID": "A原子性：事务要么全成功要么全回滚,通过undo log实现(回滚段)。C一致性：事务前后数据满足约束(是目标,由AID共同保证)。I隔离性：并发事务互不干扰,通过MVCC(ReadView+undo log版本链)和锁实现。D持久性：事务提交后数据永久保存,通过redo log实现(Write-Ahead Logging,先写日志再写磁盘)。",
    "SQL优化": "①避免SELECT *,只查需要的列(减少网络传输和内存) ②合理建索引,用EXPLAIN验证 ③避免WHERE中对字段函数运算 ④小表驱动大表(IN子查询小表在外) ⑤LIMIT深分页优化(用id>offset方式) ⑥避免隐式类型转换 ⑦批量INSERT代替逐条 ⑧合理使用JOIN替代子查询 ⑨开启慢查询日志定位慢SQL(long_query_time)",
    "explain": "关键字段：type(访问效率从好到差:system>const>eq_ref>ref>range>index>ALL) key(实际使用的索引) rows(预估扫描行数,越小越好) Extra(Using index=覆盖索引好; Using filesort=文件排序需优化; Using temporary=临时表需优化) key_len(索引使用的字节数,判断联合索引用了几列)",
    "三大范式": "1NF：字段不可再分(原子性,如地址应拆为省市区) 2NF：非主键完全依赖主键(消除部分依赖,如订单详情表中商品名应依赖商品ID而非订单ID) 3NF：非主键不能传递依赖主键(消除传递依赖,如表中有dept_id和dept_name,dept_name传递依赖于emp_id应拆表)。实际开发适当反范式化(冗余字段)提升查询性能。",
    "MySQL.*主键": "每张InnoDB表必须有主键。原因：①聚簇索引基于主键组织数据,无主键则InnoDB选一个唯一非空索引,都没有则自动生成隐藏row_id ②主键是聚簇索引的key,数据按主键顺序物理存储 ③二级索引的叶子节点存主键值(回表依据)。推荐：自增整数主键(插入有序,不频繁分裂页)。",
    "乐观锁.*悲观锁": "悲观锁：假设会冲突,先加锁再操作(SELECT ... FOR UPDATE/LOCK IN SHARE MODE)。乐观锁：假设不冲突,提交时检测冲突(版本号/CAS)。乐观锁实现：表加version字段,UPDATE SET ... WHERE id=? AND version=?,影响行数=0则重试。适用：读多写少用乐观锁,写多用悲观锁。",

    # === Redis ===
    "Redis数据类型": "5种基本类型：①String(字符串,最常用,缓存/计数器/分布式锁) ②List(双向链表,消息队列/最新列表) ③Hash(哈希表,对象属性存储) ④Set(无序集合,去重/交并差集) ⑤ZSet(有序集合,跳表+哈希实现,排行榜/延迟队列)。高级类型：Bitmap(签到/在线状态)、HyperLogLog(基数统计,UV计数)、GeoSpatial(地理位置)、Stream(消息队列,支持消费者组)。",
    "缓存雪崩": "大量缓存同时过期或Redis宕机,请求全部打到数据库。解决：①随机过期时间(加随机偏移量) ②多级缓存(本地缓存Caffeine+Redis) ③限流降级(令牌桶/滑动窗口) ④Redis高可用(Sentinel哨兵/Cluster集群) ⑤缓存预热(上线前加载热点数据) ⑥永不过期+后台异步更新",
    "缓存击穿": "热点key突然过期,大量并发请求同时打到数据库。解决：①互斥锁(SETNX,只允许一个线程重建缓存,其他线程等待或返回旧值) ②逻辑过期(在value中存过期时间,发现过期则异步更新,先返回旧值) ③永不过期(不设TTL,由后台定时更新) ④热点数据永不过期+异步刷新",
    "缓存穿透": "查询数据库中不存在的数据,缓存永远命不中。解决：①布隆过滤器(Bloom Filter,在缓存前拦截不存在的key) ②缓存空值(SET key null EX 60,短过期时间) ③接口参数校验(过滤非法请求) ④布隆过滤器+缓存空值组合使用效果最佳",
    "Redis持久化": "RDB：定时fork子进程生成dump.rdb快照。优势：恢复快、文件小。劣势：可能丢失最后一次快照后的数据。AOF：追加写命令到appendonly.aof。三种策略：always(每条)、everysec(每秒,推荐)、no(由OS决定)。AOF重写：后台重写压缩。混合持久化(RDB+AOF)：RDB做全量+AOF做增量,兼顾速度和安全。",
    "分布式锁": "Redis分布式锁：SET key uuid NX EX 30(原子操作,设置值+过期时间)。释放锁：Lua脚本(先比较value是否是自己的uuid,再DEL,保证原子性)。问题及解决：①锁超时→Redisson看门狗机制自动续期 ②不可重入→Redisson的可重入锁(Hash结构记录重入次数) ③主从不一致→RedLock(向N个独立Redis实例加锁,多数成功才算获取锁)",
    "Redis和MySQL.*一致": "①Cache Aside Pattern(旁路缓存)：读→先缓存→miss则查DB并写缓存 写→先更新DB→再删除缓存 ②延迟双删：写DB→删缓存→延迟N毫秒→再删缓存(防止并发读写导致脏数据) ③Canal监听binlog异步更新缓存 ④最终一致性：设合理过期时间兜底。推荐方案：先更新DB+再删缓存+重试机制。",
    "Redis.*淘汰策略": "8种淘汰策略：①noeviction(不淘汰,写操作报错) ②allkeys-lru(所有key中最近最少使用,最常用) ③volatile-lru(仅过期key中LRU) ④allkeys-lfu(所有key中最不经常使用) ⑤volatile-lfu ⑥allkeys-random(随机) ⑦volatile-random ⑧volatile-ttl(淘汰TTL最小的)。推荐：allkeys-lru或allkeys-lfu。配置：maxmemory-policy allkeys-lru",

    # === Spring ===
    "IOC": "IOC(控制反转)：将对象创建和依赖管理的控制权从程序代码转移到Spring容器。DI(依赖注入)是IOC的实现方式：①构造器注入(推荐,保证不可变) ②Setter注入(可选依赖) ③字段注入(@Autowired,不推荐,难以测试)。好处：解耦(面向接口编程)、便于单元测试(可注入Mock)、统一管理生命周期。",
    "AOP": "AOP(面向切面编程)：将横切关注点(日志、事务、权限、缓存)从业务逻辑中分离。核心概念：切面(Aspect=切点+通知)、连接点(JoinPoint=方法执行点)、切入点(Pointcut=匹配表达式)、通知(Advice=Before/After/Around/AfterReturning/AfterThrowing)。底层实现：接口用JDK动态代理(Proxy.newProxyInstance)，类用CGLIB(生成子类字节码)。Spring默认：有接口用JDK代理,无接口用CGLIB。Spring Boot 2.x默认全部用CGLIB。",
    "Spring设计模式": "①工厂模式：BeanFactory/ApplicationContext创建Bean ②单例模式：Bean默认singleton作用域 ③代理模式：AOP的JDK/CGLIB动态代理 ④模板模式：JdbcTemplate/RestTemplate/TransactionTemplate ⑤观察者模式：ApplicationEvent/ApplicationListener事件机制 ⑥适配器模式：HandlerAdapter适配不同类型的Handler ⑦装饰器模式：BeanWrapper ⑧策略模式：Resource/InstantiationStrategy",
    "循环依赖": "Spring通过三级缓存解决setter注入的循环依赖。一级缓存singletonObjects(完整Bean) 二级缓存earlySingletonObjects(早期引用,可能是代理对象) 三级缓存singletonFactories(ObjectFactory,用于生成早期引用)。流程：A创建中→需要B→B创建中→需要A→从三级缓存获取A的早期引用→B完成→A完成。构造器注入无法解决(需要完整对象)。Spring Boot 2.6+默认禁止循环依赖。",
    "Spring.*常用注解": "@Component(通用组件) @Service(服务层) @Repository(数据层,自动转换异常) @Controller/@RestController(Web层) @Autowired(自动注入) @Qualifier(指定Bean名称) @Scope(作用域) @Configuration(配置类) @Bean(注册Bean) @Value(注入配置) @Transactional(事务) @Aspect(切面) @Scheduled(定时任务) @Conditional(条件装配)",
    "Spring.*事务": "@Transactional注解。属性：propagation(传播行为,默认REQUIRED)、isolation(隔离级别,默认DEFAULT用数据库的)、rollbackFor(回滚异常类型,默认RuntimeException)、readOnly、timeout。传播行为：REQUIRED(有就加入没有就新建) REQUIRES_NEW(总是新建) NESTED(嵌套事务)。坑：①同类方法调用不走代理,事务失效 ②rollbackFor不指定,checked异常不回滚 ③private方法不生效",

    # === SpringBoot ===
    "SpringBoot自动配置": "@SpringBootApplication = @SpringBootConfiguration + @EnableAutoConfiguration + @ComponentScan。原理：@EnableAutoConfiguration → 通过SpringFactoriesLoader加载META-INF/spring.factories中的自动配置类 → @Conditional条件装配(如@ConditionalOnClass、@ConditionalOnMissingBean) → 满足条件则配置生效。starter机制：引入starter依赖自动引入相关自动配置。",
    "SpringBoot.*好处": "①约定优于配置,减少XML和样板代码 ②内嵌Tomcat/Jetty/Undertow,打jar直接运行 ③自动配置(条件装配+starter) ④Actuator生产级监控 ⑤外部化配置(yml/properties/环境变量优先级) ⑥快速启动(自动配置+组件扫描)。本质：不是新技术,是Spring的脚手架,简化了Spring应用的搭建和开发过程。",
    "SpringBoot.*yml": "配置文件加载优先级(从高到低)：①命令行参数 ②JNDI属性 ③系统环境变量 ④application-{profile}.yml ⑤application.yml ⑥@PropertySource ⑦默认属性。yml和properties的区别：yml支持层级结构更清晰,properties是扁平键值对。多环境：spring.profiles.active=dev激活application-dev.yml。",

    # === SpringCloud ===
    "Gateway": "Spring Cloud Gateway：基于WebFlux+Netty的响应式API网关。三大核心：Route(路由=id+uri+predicate+filter)、Predicate(断言,匹配请求条件)、Filter(过滤器,修改请求/响应)。内置断言：Path、Method、Header、Query、Cookie、After/Before/Between(时间)。内置过滤器：AddRequestHeader、StripPrefix、Retry、RateLimiter。比Zuul1.x性能更好(非阻塞vs阻塞)。",
    "Feign": "声明式HTTP客户端,简化微服务间调用。使用：@FeignClient(name=\"service-name\")定义接口,注入后像调本地方法一样调远程服务。底层：动态代理→构造HTTP请求→通过Ribbon负载均衡→发送请求。集成：Ribbon(负载均衡)、Sentinel/Hystrix(熔断降级)、OkHttpClient/HttpClient(HTTP客户端)。fallback降级：@FeignClient(fallback=xxx.class)",
    "Nacos": "阿里开源的注册中心+配置中心。注册中心：服务启动时注册→定时心跳续约(5s)→15s未收到标记不健康→30s未收到剔除。服务发现：客户端定时拉取+服务端主动推送(UDP)。配置中心：支持Namespace/Group/DataId三级隔离,动态刷新(@RefreshScope),灰度发布,配置版本回滚。CP/AP切换：临时实例用AP(Distro协议),持久实例用CP(Raft协议)。",
    "Eureka": "Netflix开源的注册中心(AP设计)。服务注册：启动时注册到Eureka Server。心跳续约：每30s发送心跳。服务剔除：90s未收到心跳则剔除(自我保护模式下不剔除)。自我保护：15分钟内心跳比例低于85%则进入保护模式,不剔除任何实例(防止网络分区误判)。客户端缓存：即使Eureka挂掉,客户端仍可用缓存的服务列表。",
    "SpringCloud.*组件": "①注册中心：Nacos(推荐)/Eureka/Consul/Zookeeper ②配置中心：Nacos(推荐)/Config/Apollo ③网关：Gateway(推荐)/Zuul ④远程调用：OpenFeign ⑤负载均衡：LoadBalancer(推荐)/Ribbon ⑥熔断降级：Sentinel(推荐)/Hystrix ⑦分布式事务：Seata ⑧消息总线：Spring Cloud Bus ⑨链路追踪：Sleuth+Zipkin/SkyWalking",
    "熔断": "熔断器模式：当服务调用失败率达到阈值时,自动切断请求(返回降级结果),防止故障蔓延。三状态：CLOSED(正常)→失败率超阈值→OPEN(熔断,直接降级)→超时后→HALF-OPEN(试探,放少量请求)→成功→CLOSED 失败→OPEN。Sentinel配置：@SentinelResource(value=\"xxx\", fallback=\"fallbackMethod\")。与降级区别：熔断是自动触发,降级是手动/兜底策略。",

    # === MyBatis ===
    "#和$区别": "#{}是预编译处理,参数替换为?占位符,由PreparedStatement设置参数,防止SQL注入。${}是字符串替换,直接拼接到SQL中,存在SQL注入风险。原则：参数值用#{},动态表名/列名/排序字段用${}(需白名单校验)。示例：WHERE name = #{name} → WHERE name = ?; ORDER BY ${column} → ORDER BY create_time",
    "resultType和resultMap": "resultType：自动映射(列名=属性名,或下划线转驼峰),简单场景用。resultMap：手动映射(column→property),复杂场景用(一对多collection/多对一association/鉴别器discriminator)。性能无差别。列名和属性名不一致时必须用resultMap。resultMap可复用,适合复杂对象映射。",
    "MyBatis.*缓存": "一级缓存：SqlSession级别,默认开启,同一SqlSession中相同查询直接返回缓存。执行增删改或commit/close后清空。二级缓存：Mapper级别(跨SqlSession),需手动开启(<cache/>),同一namespace共享。执行顺序：二级缓存→一级缓存→数据库。问题：多表关联查询时,一个表的修改不会清另一个表的二级缓存,导致脏读。Spring整合后一级缓存失效(每次请求新SqlSession)。",
    "MyBatis.*动态SQL": "9种标签：<if test=\"\">条件判断 <choose>/<when>/<otherwise>多选一 <where>自动处理AND/OR前缀 <set>自动处理逗号后缀 <trim>自定义前缀后缀 <foreach>遍历集合(IN/批量插入) <sql>/<include>SQL片段复用 <bind>变量绑定。底层：OGNL表达式解析,动态拼接SQL字符串。",

    # === JVM ===
    "JVM内存区域": "5大区域：①堆(Heap)：对象实例,GC主战场,分新生代(Eden+Survivor×2)+老年代 ②方法区/元空间(Metaspace,JDK8+)：类信息、常量池、静态变量(本地内存,不受JVM堆大小限制) ③虚拟机栈：线程私有,每个方法一个栈帧(局部变量表、操作数栈、动态链接、返回地址) ④本地方法栈：Native方法 ⑤程序计数器：当前线程执行的字节码行号(唯一不会OOM的区域)",
    "垃圾回收": "算法：①标记-清除(碎片多) ②标记-复制(浪费空间,新生代用,Eden:Survivor=8:1:1) ③标记-整理(无碎片但慢,老年代用) ④分代收集(新生代用复制,老年代用标记整理)。收集器：Serial(单线程) ParNew(多线程新生代) Parallel Scavenge(吞吐量优先) CMS(低延迟,标记-清除) G1(分Region,JDK9默认) ZGC(超低延迟,JDK15+)。JDK8默认Parallel Scavenge+Parallel Old。",
    "OOM": "①Java Heap Space：对象太多/内存泄漏(加大-Xmx/-Xms,或排查泄漏) ②Metaspace：动态生成太多类(如CGLIB代理,加大-XX:MaxMetaspaceSize) ③GC Overhead Limit Exceeded：GC时间超98%但回收不到2%内存 ④Direct Buffer Memory：NIO直接内存溢出(加大-XX:MaxDirectMemorySize) ⑤StackOverflowError：递归太深(加大-Xss) ⑥unable to create new native thread：线程数超系统限制",
    "JVM调优": "常用参数：-Xms/-Xmx(堆大小,建议相等) -Xmn(新生代大小) -XX:MetaspaceSize -XX:+UseG1GC -XX:MaxGCPauseMillis(G1目标停顿) -XX:+PrintGCDetails(打印GC日志) -XX:+HeapDumpOnOutOfMemoryError(OOM时dump)。工具：jps(查看Java进程) jstat(GC统计) jmap(堆dump) jstack(线程dump) Arthas(在线诊断)。调优目标：低延迟/高吞吐/低OOM。",
    "双亲委派": "类加载器层级：Bootstrap(加载rt.jar等核心类) → Extension(加载ext目录) → Application(加载classpath) → 自定义。工作流程：收到加载请求→先委托父加载器→父加载器找不到→自己加载。好处：①避免重复加载 ②安全(防止自定义java.lang.String覆盖核心类)。打破：重写loadClass()或线程上下文类加载器(如JDBC/SPI)。",

    # === 消息队列 ===
    "Kafka": "分布式流处理平台。核心概念：Producer(生产者)、Consumer(消费者)、Broker(服务器)、Topic(主题)、Partition(分区,有序)、Offset(消费位移)、ConsumerGroup(消费者组,组内竞争消费)。消息不丢失：producer(acks=all,retries=Integer.MAX_VALUE,min.insync.replicas≥2) broker(replication.factor≥3,unclean.leader.election.enable=false) consumer(enable.auto.commit=false,手动提交offset)。顺序：同一Partition内有序(相同key路由到同一Partition)。",
    "Kafka.*RabbitMQ": "Kafka：高吞吐、分布式、持久化、Pull模式(消费者主动拉取)、适合大数据/日志/流处理。RabbitMQ：低延迟、AMQP协议、Push模式(推送给消费者)、支持复杂路由(Exchange+Binding)、适合业务消息。选型：大数据量/日志/流处理→Kafka 业务消息/延迟队列/复杂路由→RabbitMQ",
    "消息丢失": "①生产者丢失：同步发送+重试机制,异步发送用回调确认 ②Broker丢失：Kafka设置acks=all+replication≥3+min.insync.replicas≥2; RabbitMQ开启持久化+confirm模式 ③消费者丢失：关闭自动提交offset,处理完再手动提交; RabbitMQ关闭自动ACK,处理完再手动ACK。消息持久化：Kafka写磁盘(commit log),RabbitMQ持久化到磁盘(queue持久化+message持久化)。",
    "消息队列.*重复": "幂等性保证：①数据库唯一索引(消息ID去重) ②Redis SET NX(消息ID设标记) ③状态机(业务状态只能单向流转) ④乐观锁(版本号)。消费端：先查询再操作,保证重复消费结果一致。Kafka：enable.auto.commit=false,处理完再commit,配合业务幂等。RabbitMQ：手动ACK+消息ID去重表。",

    # === Elasticsearch ===
    "ES.*原理": "基于Lucene的分布式全文搜索引擎。核心概念：Index(索引)→Document(文档)→Field(字段)。倒排索引：文档→分词→建立\"词项→文档ID列表\"的映射。搜索时：查询词→分词→查找倒排索引→合并结果→打分排序(TF-IDF/BM25)。集群：Master节点(集群管理)、Data节点(存储数据)、Coordinating节点(请求路由)。",
    "ES.*MySQL.*同步": "①同步双写：业务代码同时写MySQL和ES(简单但耦合高,有一致性风险) ②异步双写：写MySQL后发MQ消息,消费者写ES(解耦,最终一致) ③Canal监听binlog：Canal伪装MySQL从库→监听binlog→同步到ES(无侵入,推荐) ④定时任务：定时查MySQL更新ES(延迟大,适合非实时场景)。推荐：Canal+MQ(无侵入+可靠投递)。",

    # === Docker与DevOps ===
    "Docker": "容器化平台,核心概念：镜像(Image,只读模板)、容器(Container,镜像的运行实例)、仓库(Registry,如Docker Hub)。常用命令：docker run(build/run/stop/rm/ps/logs/exec) Dockerfile：FROM(基础镜像) RUN(构建时执行) COPY/ADD(复制文件,ADD支持URL和自动解压) CMD/ENTRYPOINT(启动命令) EXPOSE(声明端口) WORKDIR(工作目录) VOLUME(挂载卷)。镜像分层：每条指令一层,共享基础层节省空间。",
    "Docker.*ADD.*COPY": "COPY：只做文件复制,从构建上下文复制到镜像。ADD：除了复制还支持①URL自动下载 ②tar文件自动解压。最佳实践：优先用COPY(行为明确),需要解压tar时用ADD。COPY --chown=user:group可设置文件所有者。",
    "Linux.*命令": "常用：ls -la(列文件) cd/pwd(目录) cp/mv/rm(文件操作) mkdir -p(递归创建) cat/less/tail -f(查看文件) grep -rn(搜索) find(查找) chmod/chown(权限) ps aux/top(进程) netstat -tlnp/ss -tlnp(端口) df -h(磁盘) free -m(内存) tar -xzvf(解压) curl(请求) vim(编辑)。",
    "nginx": "高性能HTTP和反向代理服务器。用途：①反向代理(proxy_pass) ②负载均衡(upstream,轮询/权重/ip_hash/least_conn) ③静态资源服务 ④HTTPS终端(SSL证书配置)。常用配置：server块(虚拟主机) location块(路由匹配) proxy_pass(转发)。启动/停止：nginx -s reload(热重载) nginx -s stop(停止)。",

    # === 设计模式 ===
    "单例模式": "5种实现：①饿汉式：static final实例,类加载时创建,线程安全 ②懒汉式：synchronized方法,线程安全但性能差 ③双重检查锁：volatile+synchronized块,需volatile防止指令重排 ④静态内部类：利用类加载机制保证线程安全(推荐) ⑤枚举：最安全,防反射和序列化攻击(Effective Java推荐)。Spring Bean默认单例(容器管理)。",
    "工厂模式": "①简单工厂：一个工厂类根据参数创建不同产品(违反开闭原则) ②工厂方法：每个产品一个工厂,符合开闭原则 ③抽象工厂：创建一组相关产品(产品族)。Spring中的应用：BeanFactory是工厂模式,FactoryBean是工厂方法模式。实际开发中,简单工厂最常用(if-else/switch或Map+反射)。",
    "代理模式": "为其他对象提供代理以控制访问。静态代理：编译时确定,实现同一接口。动态代理：运行时生成代理类。JDK动态代理：基于接口(Proxy.newProxyInstance+InvocationHandler)。CGLIB代理：基于继承(生成子类字节码,无需接口)。Spring AOP默认：有接口→JDK代理,无接口→CGLIB(Spring Boot 2.x默认全部CGLIB)。",

    # === 分布式 ===
    "分布式事务": "CAP定理：一致性、可用性、分区容错性不可兼得(最多满足两个)。方案：①2PC(两阶段提交,强一致但性能差) ②TCC(try-confirm-cancel,业务侵入大) ③Saga(长事务,补偿机制) ④本地消息表(最终一致) ⑤MQ事务消息(如RocketMQ) ⑥Seata(推荐,支持AT/TCC/Saga/XA模式)。Seata AT模式：一阶段提交本地事务+写undo log,二阶段提交则删除undo log/回滚则用undo log反向补偿。",
    "分布式锁": "实现方式：①Redis(SET NX EX,释放用Lua脚本,Redisson生产级实现) ②Zookeeper(临时顺序节点+Watch,公平锁,Curator实现) ③数据库(唯一索引/悲观锁)。对比：Redis性能最好但主从切换可能丢锁;Zookeeper最可靠但性能稍差;数据库最简单但性能最差。推荐：Redis+Redisson(看门狗续期+可重入+RedLock)。",

    # === 项目与场景 ===
    "JWT": "JSON Web Token三部分(用.分隔)：①Header(算法类型,如HS256) ②Payload(用户信息,如userId/角色/过期时间) ③Signature(签名,HMAC-SHA256(header+payload+secret))。特点：无状态(服务端不存session)、可扩展、跨域支持。过期处理：①前端拦截401跳登录 ②Refresh Token机制(短access token+长refresh token) ③滑动过期(每次访问刷新)。vs Session：JWT存在客户端,Session存在服务端。",
    "登录流程": "典型流程：①前端提交用户名+密码(HTTPS加密传输) ②后端校验(BCrypt加密比较密码哈希) ③校验通过生成JWT Token返回 ④前端存储Token(localStorage/HttpOnly Cookie) ⑤后续请求携带Token(Authorization: Bearer xxx) ⑥拦截器校验Token有效性(签名+过期时间) ⑦Token过期返回401,前端跳登录或用Refresh Token刷新。安全：密码BCrypt加密存储,Token设合理过期时间,敏感操作二次验证。",
    "单点登录": "SSO：一次登录,所有系统共享认证。CAS流程：①用户访问A系统 ②A发现未登录→重定向到SSO认证中心 ③用户在SSO登录→生成Ticket→重定向回A(带Ticket) ④A向SSO验证Ticket→创建本地会话 ⑤访问B系统→B重定向到SSO→SSO发现已登录→直接给Ticket→B验证→创建本地会话。技术实现：Spring Security OAuth2/CAS/Shiro+Redis共享Session。",
    "高并发": "①缓存(Redis/本地缓存Caffeine减少DB压力) ②异步(消息队列削峰填谷) ③限流(令牌桶/滑动窗口算法,如Sentinel) ④降级(返回兜底数据/默认值) ⑤熔断(快速失败,防止级联故障) ⑥负载均衡(Nginx/LB分发请求) ⑦数据库优化(读写分离/分库分表/索引优化) ⑧CDN(静态资源加速) ⑨池化(线程池/连接池复用资源) ⑩集群(水平扩展)。",
    "git冲突": "解决步骤：①git pull获取最新代码 ②发现冲突文件(<<<<<<< HEAD标记) ③手动编辑冲突文件,保留正确代码,删除冲突标记 ④git add标记冲突已解决 ⑤git commit提交合并 ⑥git push。预防：①频繁pull/fetch保持同步 ②小粒度频繁提交 ③功能分支开发,减少冲突范围 ④团队约定代码规范和分支策略。",
    "幂等性": "同一操作执行一次和多次结果相同。实现：①Token机制(请求前获取唯一Token,服务端校验+删除) ②数据库唯一索引(防止重复插入) ③乐观锁/版本号(UPDATE WHERE version=N) ④状态机(状态只能单向流转) ⑤去重表(业务ID唯一)。场景：支付回调(可能重复通知)、接口重试、消息重复消费。",

    # === JVM补充 ===
    "类加载": "加载→验证→准备→解析→初始化。加载：通过类全名获取二进制字节流,生成Class对象。验证：文件格式/元数据/字节码/符号引用验证。准备：为类变量分配内存并设零值(static int a=10→此时a=0)。解析：符号引用→直接引用。初始化：执行<clinit>(static块+static变量赋值)。触发初始化：new/getstatic/putstatic/invokestatic/反射/子类触发父类/main方法。",
    "GC Roots": "可达性分析算法的根节点。GC Roots包括：①虚拟机栈中引用的对象(局部变量) ②方法区中静态变量引用的对象 ③方法区中常量引用的对象 ④本地方法栈中JNI引用的对象 ⑤JVM内部的引用(如基本类型的Class对象) ⑥被同步锁持有的对象。从GC Roots出发,不可达的对象即为垃圾。",
    "强引用.*软引用.*弱引用": "①强引用(Strong)：Object o=new Object(),不会被GC回收(除非置null) ②软引用(Soft)：内存不足时才回收,适合缓存(SoftReference) ③弱引用(Weak)：下次GC时一定回收,适合不影响生命周期的缓存(WeakReference,如WeakHashMap) ④虚引用(Phantom)：随时可能被回收,仅用于跟踪对象被回收的时机(PhantomReference+ReferenceQueue)。",

    # === 多线程补充 ===
    "CAS": "Compare And Swap,比较并交换。三个操作数：内存值V、期望值A、新值B。当V==A时,将V更新为B,否则不做任何操作(返回当前值重试)。是乐观锁的底层实现。Java中通过Unsafe类的compareAndSwapInt/native方法实现(基于CPU的CAS指令)。ABA问题：A→B→A,CAS认为没变。解决：AtomicStampedReference(加版本号)。自旋开销：CAS失败会一直重试,可用LongAdder替代AtomicLong减少竞争。",
    "AQS": "AbstractQueuedSynchronizer,抽象队列同步器。是ReentrantLock/Semaphore/CountDownLatch等并发工具的底层框架。核心：volatile int state(同步状态) + CLH双向队列(等待线程)。ReentrantLock：state=0未锁/>0已锁(可重入计数)。获取锁：CAS设state→失败→入队→park阻塞。释放锁：state减→为0则唤醒队头线程。公平锁/非公平锁：公平锁入队前检查队列,非直接CAS抢。",
    "CountDownLatch.*CyclicBarrier": "CountDownLatch：一次性计数器,await()等待计数归零,countDown()减一。场景：主线程等N个子线程完成。CyclicBarrier：可重用栅栏,所有线程到达栅栏后一起继续。场景：多线程分段计算后合并。区别：CountDownLatch一次性的且是主线程等子线程;CyclicBarrier可重用且是子线程之间互等。Semaphore：信号量,控制并发访问数(acquire获取/permit释放)。",

    # === 补充 ===
    "过滤器.*拦截器": "过滤器(Filter)：Servlet规范,基于函数回调,在Servlet前后执行。拦截器(Interceptor)：Spring MVC,基于Java反射(AOP),在Handler前后执行。执行顺序：Filter→Interceptor→Controller→Interceptor→Filter。Filter能拿到request/response但拿不到handler信息;Interceptor能拿到handler(如方法名/注解)。Filter在web.xml或@WebFilter配置;Interceptor实现HandlerInterceptor注册到WebMvcConfigurer。拦截器3个方法：preHandle(前)→postHandle(后)→afterCompletion(视图渲染后,无论成功失败)。",
    "mybatis-plus.*mybatis": "MyBatis：手写SQL,灵活控制,适合复杂SQL。MyBatis-Plus：MyBatis的增强工具,提供CRUD接口(继承BaseMapper即可),内置分页插件/代码生成器/逻辑删除/自动填充/乐观锁。优点：减少样板代码,单表操作零SQL。缺点：复杂联表查询仍需手写SQL,Wrapper条件构造器可读性差(不如直接写SQL清晰)。建议：简单CRUD用MP,复杂SQL手写XML。",
    "Redis.*应用场景": "①缓存(热点数据,减少DB压力) ②分布式锁(SET NX EX) ③排行榜(ZSet+score) ④计数器(incr/decr,如阅读量) ⑤限流(滑动窗口/令牌桶) ⑥延迟队列(ZSet+score为执行时间) ⑦Session共享(分布式系统登录态) ⑧布隆过滤器(防缓存穿透) ⑨地理空间(GEO,附近的人) ⑩消息队列(List/Stream) ⑪分布式ID(Redis INCR自增) ⑫热点数据统计(HyperLogLog UV计数)",
    "SpringMVC.*流程": "①客户端请求→DispatcherServlet(前端控制器) ②DispatcherServlet→HandlerMapping查找Handler(根据URL找到对应的Controller方法) ③返回HandlerExecutionChain(Handler+拦截器链) ④DispatcherServlet→HandlerAdapter执行Handler ⑤执行Controller方法(参数绑定/校验/业务逻辑) ⑥返回ModelAndView ⑦ViewResolver解析视图 ⑧渲染视图→响应客户端。前后端分离后：Controller直接返回JSON(@ResponseBody),跳过视图解析。",
    "String.*常用方法": "charAt(i)、length()、substring(begin[,end])、indexOf(str)、lastIndexOf(str)、contains(str)、startsWith(str)、endsWith(str)、trim()、toUpperCase()/toLowerCase()、replace(old,new)、split(regex)、toCharArray()、equals(str)、equalsIgnoreCase(str)、compareTo(str)、isEmpty()、isBlank()(JDK11+)、valueOf()(其他类型转String)、format()(格式化)、strip()(JDK11+,去除首尾空白,支持Unicode)",
}

def find_answer(question, category):
    q = question.lower()
    best_match = None
    best_score = 0
    for keyword, answer in detailed_answers.items():
        kw = keyword.lower()
        if kw in q or q in kw:
            score = len(kw)
            if score > best_score:
                best_score = score
                best_match = answer
    if best_match:
        return best_match
    
    # Category fallback
    return ""

# Apply answers
updated = 0
for q in data:
    new_answer = find_answer(q['question'], q['category'])
    if new_answer:
        q['answer'] = new_answer
        updated += 1
    elif not q['answer'] or '暂无标准答案' in q['answer'] or '通用参考' in q['answer']:
        # Keep existing good answers, only replace bad ones
        q['answer'] = ""

with open('public/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Updated {updated} answers with detailed content")
print(f"Total questions: {len(data)}")

# Count answers
has_answer = sum(1 for q in data if q['answer'])
print(f"With answer: {has_answer} ({has_answer*100//len(data)}%)")
