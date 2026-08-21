import json, re

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

more_answers = {
    # InnoDB/MySQL深入
    "多版本控制": "InnoDB MVCC(多版本并发控制)。每行有隐藏字段trx_id(最后修改事务ID)+roll_pointer(指向undo log旧版本)。ReadView记录当前活跃事务列表。读取时：如果行的trx_id<ReadView.min_trx_id→可见;>max_trx_id→不可见;在之间→检查是否在活跃列表中。RC级别每次SELECT生成新ReadView,RR级别只第一次生成。实现无锁读(快照读),写操作仍需行锁。",
    "MVCC": "Multi-Version Concurrency Control。InnoDB每行有trx_id+roll_pointer隐藏字段。undo log形成版本链。ReadView判断可见性。RC每次SELECT新ReadView,RR只第一次SELECT生成。实现：读不阻塞写,写不阻塞读。快照读(SELECT)无锁,当前读(SELECT FOR UPDATE/INSERT/UPDATE/DELETE)需加锁。",

    # 序列化
    "序列化": "Java序列化：将对象转为字节流(实现Serializable接口,ObjectOutputStream.writeObject())。反序列化：字节流→对象(ObjectInputStream.readObject())。transient关键字排除字段。serialVersionUID版本控制(反序列化时校验)。问题：不安全(反序列化漏洞)/性能差/跨语言不行。替代：JSON(Jackson/Gson)/Protobuf/Hessian/Kryo。",

    # 网络协议
    "https": "HTTPS=HTTP+TLS/SSL。加密过程(握手)：①Client Hello(支持的TLS版本/加密套件/随机数) ②Server Hello(选定套件/证书/随机数) ③客户端验证证书(证书链→CA根证书) ④客户端生成预主密钥→用服务器公钥加密发送 ⑤双方用三个随机数生成会话密钥(对称加密) ⑥后续通信用对称加密。vs HTTP：加密传输(防窃听)/身份验证(防中间人)/端口443。",
    "http.*协议": "HTTP协议：应用层,请求-响应模型。请求：方法(GET/POST/PUT/DELETE)+URL+Headers+Body。响应：状态码(200成功/301重定向/404未找到/500服务器错误)+Headers+Body。版本：HTTP/1.1(持久连接/管道)/HTTP/2(多路复用/头部压缩/服务器推送)/HTTP/3(QUIC,基于UDP)。",
    "tcp": "TCP传输控制协议,面向连接/可靠/字节流。三次握手：SYN→SYN+ACK→ACK(建立连接)。四次挥手：FIN→ACK→FIN→ACK(关闭连接)。可靠机制：序列号+确认号/超时重传/流量控制(滑动窗口)/拥塞控制(慢启动/拥塞避免/快重传/快恢复)。vs UDP：TCP可靠有序/UDP无连接不可靠但快(DNS/视频流/游戏)。",

    # 消息队列深入
    "消息积压": "消费者处理速度跟不上生产者。解决：①增加消费者数量(扩容) ②增加消费者并发(多线程消费) ③优化消费逻辑(减少IO/批量处理) ④跳过非关键消息 ⑤临时扩容(紧急增加消费者机器) ⑥限流(控制生产速度)。根本原因：消费者代码慢/消费者数量不足/突发流量。监控：消费延迟(Consumer Lag)告警。",
    "重复消费": "消息被消费多次。原因：消费者处理完但ACK前崩溃→Broker重新投递。解决：幂等性保证。方案：①数据库唯一索引(消息ID去重) ②Redis SET NX(消息ID标记已处理) ③状态机(业务状态只能单向流转) ④乐观锁(版本号) ⑤去重表(消费前查重)。Kafka：enable.auto.commit=false+手动提交+业务幂等。",

    # 网络/分布式
    "脑裂": "集群中因网络分区导致出现多个\"主节点\"。原因：网络分区→部分节点认为主节点宕机→选举新主→出现双主(脑裂)→数据不一致。解决：①法定人数(Quorum)：多数节点同意才能选主(如ZAB/Raft) ②Fencing机制(旧主发现连不上多数节点→主动退出) ③Lease机制(租约过期→旧主降级) ④STONITH(Shoot The Other Node In The Head)。Zookeeper用ZAB协议防脑裂。",
    "网络分区": "分布式集群中网络故障导致节点间无法通信。CAP定理：发生分区时必须在C(一致性)和A(可用性)之间选择。CP系统(如Zookeeper)：分区时拒绝写入保证一致性。AP系统(如Eureka)：分区时继续服务但可能不一致。实际：大多数系统选择AP+最终一致性。",

    # MyBatis Plus
    "MP.*查询": "MyBatis-Plus查询：①QueryWrapper链式调用(wrapper.gt(\"id\",10).orderByDesc(\"create_time\")) ②LambdaQueryWrapper(类型安全,lambda写法:wrapper.gt(User::getId,10)) ③分页(Page对象+分页插件) ④自定义SQL(@Select注解或XML)。Wrapper：eq/ne/gt/ge/lt/le/like/in/between/orderBy/groupBy。",
    "selectOne": "MyBatis-Plus BaseMapper方法。selectOne(Wrapper)：查询单条记录,结果多于一条会报错。用法：User user = userMapper.selectOne(new QueryWrapper<User>().eq(\"id\",1)); 或Lambda写法。注意：结果为空返回null,多于一条抛异常。如果确实可能多条,用selectList+limit 1。",

    # 工程实践
    "源代码管理": "Git分布式版本控制。常用命令：git clone/pull/push/add/commit/branch/merge/rebase/stash/log/diff。分支策略：Git Flow(master+develop+feature+release+hotfix)/GitHub Flow(只有main+feature分支,PR合并)/Trunk-Based(主干开发,短命分支)。推荐：小团队用GitHub Flow(简单),大团队用Git Flow(规范)。",
    "feign.*私服": "Feign客户端封装后发布到Maven私服(Nexus/Artifactory)。做法：①将Feign接口+DTO抽取为独立模块 ②打包发布到私服 ③其他服务引入依赖即可调用。好处：复用接口定义/避免每个消费者都写一遍。注意：版本管理(接口变更需同步升级版本)/DTO与服务端保持一致。",
    "excel": "Java操作Excel：①Apache POI(支持xls和xlsx,HSSFWorkbook/XSSFWorkbook) ②EasyExcel(阿里,基于POI优化,内存占用低) ③JXLS(模板导出)。注意事项：①大文件用EasyExcel/SXSSFWorkbook(流式写入,避免OOM) ②合并单元格处理 ③日期格式 ④数据类型(字符串/数字/公式) ⑤导入校验(空值/格式错误)。",

    # SSM
    "ssm": "SSM=Spring+SpringMVC+MyBatis。Spring：IOC容器+AOP。SpringMVC：MVC框架,DispatcherServlet→HandlerMapping→Controller→ViewResolver→View。MyBatis：ORM框架,SQL映射。vs SpringBoot+MyBatis-Plus：SSM需要大量XML配置,Boot自动配置+MP减少样板代码。SSM是传统Java Web开发标配,现在基本被SpringBoot取代。",
    "五大组件": "SpringMVC五大组件：①DispatcherServlet(前端控制器,接收所有请求) ②HandlerMapping(处理器映射,URL→Controller方法) ③HandlerAdapter(处理器适配,执行Controller) ④ViewResolver(视图解析器,逻辑视图→物理视图) ⑤View(视图渲染,JSP/Thymeleaf/JSON)。前后端分离后：Controller直接返回JSON(@ResponseBody),跳过ViewResolver和View。",

    # 排行榜
    "排行榜": "Redis ZSet实现排行榜。ZADD添加成员+分数,ZREVRANGE获取Top N(降序),ZREVRANK获取排名,ZINCRBY更新分数。分数相同时按字典序。实时排行榜：直接ZSet。大量数据：分片(按分数范围分多个ZSet)+聚合。持久化：定时同步到MySQL。防刷：同一用户限制更新频率/用时间衰减(新数据权重更高)。",

    # QPS/性能
    "QPS": "QPS(Queries Per Second,每秒查询数)。评估方法：①压测(JMeter/wrk/locust) ②监控(Prometheus/Grafana) ③日志分析(统计请求数/时间)。优化：①缓存(Redis/本地缓存) ②异步(MQ) ③数据库优化(索引/读写分离) ④代码优化(减少IO/批量操作) ⑤水平扩展(加机器+负载均衡) ⑥CDN(静态资源)。参考：单机MySQL~2000 QPS,Redis~10万QPS。",

    # 数据统计
    "数据统计": "数据统计方案：①实时：Redis INCR(计数器)/HyperLogLog(UV去重)/Stream(实时聚合) ②准实时：Flink流处理(窗口聚合) ③离线：Hive/Spark批处理+可视化(Grafana/Metabase)。日活/月活：Redis Bitmap(SETBIT/GETBIT)或HyperLogLog。漏斗分析：SQL多步JOIN。留存率：N日活跃用户/新增用户。",

    # 问题解决
    "遇到的问题": "回答框架：①STAR法则(Situation场景→Task任务→Action行动→Result结果) ②技术问题：描述现象→排查过程→定位原因→解决方案→预防措施 ③选择有深度的例子(不是简单bug,而是有技术挑战的) ④量化结果(性能提升XX%/错误率降低XX%)。避免：说没有遇到过问题/只说结果不说过程。",
    "如何解决": "问题解决能力展示：①复现问题(确认现象) ②缩小范围(二分法定位) ③查看日志(错误信息) ④搜索(文档/StackOverflow/AI) ⑤请教同事 ⑥尝试修复 ⑦验证 ⑧总结(文档化,避免再犯)。面试看的是思考过程,不是答案本身。",

    # 面试通用
    "介绍.*功能": "功能介绍框架：①业务背景(解决什么用户需求) ②技术方案(用了什么技术/为什么选这个) ③核心实现(关键代码/难点) ④优化(做了哪些优化) ⑤成果(量化指标)。举例：\"我负责了文章发布模块,用Redis缓存热点文章(减少DB压力),用MQ异步处理审核(提升发布速度),上线后文章发布响应时间从2s降到200ms。\"",
    "职位": "回答简洁：当前职位+核心职责+技术栈。如\"Java后端开发,主要负责XX系统的后端开发,使用SpringBoot+MySQL+Redis技术栈\"。如果有亮点可以补充(如\"独立负责了XX模块从0到1的开发\")。避免：说太多无关经历。",
    "城市": "如实回答。如果是远程/可调配,说明灵活性。这类问题面试官在评估到岗时间和稳定性。",

    # Java细节
    "fianl.*数组": "final修饰数组：数组引用不可变(不能指向新数组),但数组内容可以修改(arr[0]=10合法)。final修饰对象：引用不可变,但对象属性可以修改(除非属性也是final)。final修饰基本类型：值不可变。final数组的典型用法：方法参数中防止数组被重新赋值,但允许修改内容。",
    "数据统计做过吗": "回答：有/没有+具体说明。如果有：描述统计场景(用户行为分析/业务指标看板)+技术方案(Redis计数器/MySQL聚合/ES)+可视化(Grafana/ECharts)。如果没有：说\"虽然没有直接做,但我了解技术方案,如用Redis HyperLogLog统计UV,用Bitmap做日活统计\"。",
    "排行榜.*实现": "Redis ZSet实现：ZADD添加成员+分数→ZREVRANGE获取Top N→ZINCRBY更新分数→ZREVRANK查排名。分数相同按字典序。大规模：分片ZSet+聚合。防刷：限频+时间衰减。持久化：定时同步MySQL。替代方案：MySQL ORDER BY+索引(数据量小时)。",
    "封装好的feign": "Feign客户端封装发布到Maven私服的做法：①抽取Feign接口+DTO到独立模块 ②配置Maven发布到私服(Nexus/Artifactory) ③消费方引入依赖直接注入使用。好处：复用/版本管理/避免接口不一致。注意：接口变更需同步升级版本号,DTO保持与服务端一致。",

    # 通用技术补充
    "java.*基础": "Java基础核心：①面向对象(封装/继承/多态/抽象) ②基本类型(8种)+包装类(自动装箱拆箱) ③String(不可变,final char[]) ④异常体系(Error/RuntimeException/CheckedException) ⑤集合框架(List/Set/Map) ⑥IO(BIO/NIO/AIO) ⑦多线程(Thread/Runnable/线程池) ⑧反射/泛型/注解/Lambda ⑨JVM(内存模型/GC/类加载)。",
    "java虚拟机.*加载": "类加载过程：①加载(通过类全名获取字节流→生成Class对象) ②验证(文件格式/元数据/字节码/符号引用) ③准备(为类变量分配内存→设零值,static int a=10→此时a=0) ④解析(符号引用→直接引用) ⑤初始化(执行<clinit>,static变量赋值+static代码块)。双亲委派：先委托父加载器→找不到→自己加载。",

    # 场景补充
    "mp.*查询.*id": "MyBatis-Plus查询ID>10：QueryWrapper写法：queryWrapper.gt(\"id\",10)。Lambda写法(推荐,类型安全)：new LambdaQueryWrapper<User>().gt(User::getId,10)。链式调用：wrapper.gt(User::getId,10).orderByDesc(User::getCreateTime).last(\"LIMIT 10\")。分页：Page<User> page = new Page<>(1,10); userMapper.selectPage(page, wrapper);",
    "磁盘.*使用": "Linux查看磁盘使用：df -h(查看各分区使用率)/du -sh *(当前目录各文件夹大小)/du -sh /path(指定路径大小)。清理：①日志文件(logrotate轮转) ②临时文件(/tmp) ③Docker镜像(docker system prune) ④Maven仓库(~/.m2) ⑤Node modules。自动化：crontab定时清理+告警(磁盘>80%通知)。",
    "同时上传多个": "多文件上传：前端用<input type=\"file\" multiple>或拖拽组件(dropzone)。后端SpringBoot用MultipartFile[]数组接收。注意：①文件大小限制(spring.servlet.multipart.max-file-size) ②文件类型校验(白名单) ③异步处理(大文件用消息队列异步处理) ④存储(本地/OSS/MinIO) ⑤并发控制(限制同时上传数)。",

    # 补充答案
    "消息.*重复消费": "消息被重复消费。原因：消费者ACK前崩溃→Broker重新投递。解决：①数据库唯一索引(消息ID) ②Redis SET NX(标记已处理) ③状态机(只能单向流转) ④乐观锁(version) ⑤去重表。Kafka：手动提交offset+业务幂等。RabbitMQ：手动ACK+消息ID去重。",
    "水平分表": "水平分表(Sharding)：按行切分,不同行存不同表(如同一用户数据在同一个分片)。策略：①范围分片(按ID范围) ②哈希分片(ID%N) ③一致性哈希(增减节点影响小)。中间件：ShardingSphere(推荐,支持JDBC/Proxy)/MyCat。挑战：跨分片查询/分布式事务/全局ID(雪花算法)。分库：不同表放不同数据库(减少单库压力)。",
    "开.*发.*遇到.*问题": "回答框架(STAR)：①Situation：项目背景(如\"在做XX功能时\") ②Task：遇到的问题(如\"发现接口响应时间突然从100ms升到2s\") ③Action：排查过程(如\"用Arthas trace发现是SQL慢查询→EXPLAIN发现没走索引→添加联合索引\") ④Result：结果(如\"响应时间降回80ms,之后建立了慢查询监控\")。选有技术深度的例子。",
    "平时.*学习": "回答：①官方文档(Spring/Redis官方文档,最权威) ②源码(读优秀框架源码) ③技术博客(掘金/InfoQ) ④开源项目(GitHub) ⑤实践(个人项目/技术demo) ⑥社区(GitHub Issue/Stack Overflow) ⑦AI工具(ChatGPT辅助学习)。避免只说\"看博客\",要说具体的学习习惯和产出(如\"每周读一个开源项目的核心模块\")。",
    "数据.*存放": "数据存储选型：①MySQL(结构化数据,强事务) ②Redis(缓存/会话/排行榜) ③MongoDB(灵活Schema,文档型) ④Elasticsearch(全文检索) ⑤对象存储(文件/图片/视频→OSS/MinIO) ⑥时序数据库(监控指标→InfluxDB/Prometheus) ⑦图数据库(关系网络→Neo4j)。选型依据：数据特征/查询模式/一致性要求/规模。",
    "同时上传": "多文件上传方案：前端multiple属性或拖拽组件。后端MultipartFile[]接收。注意：大小限制/类型校验/异步处理大文件/存储(本地/OSS/MinIO)/进度条(WebSocket推送)/并发限制。大文件：分片上传(前端切片→后端合并→断点续传)。",
    "封装.*feign": "将Feign接口封装发布到私服(Nexus/Artifactory)。步骤：①创建独立Maven模块(只含Feign接口+DTO) ②pom配置distributionManagement(私服地址) ③mvn deploy发布 ④消费方引入依赖+@EnableFeignClients。好处：接口复用/版本管理/避免不一致。注意：变更需升级版本/DTO与服务端保持同步。",
}

# Apply
patterns = []
for kw, answer in more_answers.items():
    try:
        pat = re.compile(kw, re.IGNORECASE)
        patterns.append((pat, len(kw), answer))
    except:
        patterns.append((re.compile(re.escape(kw), re.IGNORECASE), len(kw), answer))
patterns.sort(key=lambda x: -x[1])

updated = 0
for q in data:
    if '建议结合项目经验' not in q.get('answer', ''):
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

with open('public/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

remaining = sum(1 for q in data if '建议结合项目经验' in q.get('answer', ''))
good = sum(1 for q in data if q['answer'] and len(q['answer']) > 100)
print(f"Updated: {updated}")
print(f"Good (>100 chars): {good} ({good*100//len(data)}%)")
print(f"Still generic: {remaining} ({remaining*100//len(data)}%)")
