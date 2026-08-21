import json, re

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

final_answers = {
    "定时任务": "Java定时任务：①Timer(简单但单线程,异常会终止) ②ScheduledExecutorService(线程池,推荐) ③Spring @Scheduled(cron表达式,最常用) ④Quartz(分布式,支持集群/持久化) ⑤XXL-Job(分布式任务调度平台,可视化管理) ⑥Spring Task+@EnableScheduling。cron：秒 分 时 日 月 周。分布式环境：用Redis分布式锁防止多实例重复执行/用XXL-Job统一调度。",
    "this指向": "Java中this指向当前对象实例。用法：①this.field区分成员变量和局部变量 ②this.method()调用当前对象其他方法 ③this()调用当前类其他构造器(必须在第一行) ④作为参数传递(回调模式)。不能在static方法中使用this(static方法属于类不属于实例)。vs JS：JS中this取决于调用方式(默认/隐式/显式/new绑定),Java中this始终指向当前实例。",
    "延迟双删.*失败": "延迟双删删除缓存失败的处理：①重试机制(删除失败→延迟重试,最多N次) ②消息队列(删除失败→发MQ消息→消费者重试删除) ③Canal兜底(Canal监听binlog→最终一致性,不依赖删除操作) ④设置合理过期时间(即使删除失败,过期后自动失效) ⑤删除改为更新(UPDATE而不是DELETE+INSERT,减少不一致窗口)。核心：延迟双删不是100%可靠,需要过期时间兜底。",
    "主从复制.*底层": "MySQL主从复制原理：①Master将数据变更写入binlog(二进制日志) ②Slave的IO线程连接Master→读取binlog→写入本地relay log(中继日志) ③Slave的SQL线程读取relay log→重放SQL→应用到Slave数据库。复制模式：异步(默认,不等Slave确认)/半同步(至少一个Slave确认)/组复制(全同步,MGR)。GTID(全局事务ID)：简化故障切换,自动定位复制位点。",
    "交换机": "RabbitMQ交换机类型：①Direct(直连,精确匹配routing key) ②Fanout(广播,忽略routing key,发到所有绑定队列) ③Topic(主题,通配符匹配,#匹配多个词,*匹配一个词) ④Headers(根据消息头匹配,少用)。默认交换机(\"\",AMQP default)：routing key=队列名,直接投递。死信交换机(DLX)：消息被拒绝/超时/队列满→路由到DLX。",
    "class.*加载": "类加载过程：①加载(Loading)：通过类全名获取字节码→方法区存类信息→堆中生成Class对象 ②验证(Verification)：文件格式/元数据/字节码/符号引用验证 ③准备(Preparation)：类变量分配内存→设零值(static int a=10→此时a=0) ④解析(Resolution)：符号引用→直接引用 ⑤初始化(Initialization)：执行<clinit>(static变量赋值+static代码块)。触发初始化：new/getstatic/putstatic/invokestatic/反射/main。",
    "数组.*扩容": "Java ArrayList扩容：默认容量10,扩容为原来的1.5倍(oldCapacity + (oldCapacity >> 1))。Arrays.copyOf()复制旧数组到新数组。初始容量：new ArrayList<>()时第一次add才创建容量10的数组。优化：如果知道数据量,用new ArrayList<>(expectedSize)避免多次扩容。数组本身(ArrayList底层Object[])不能扩容,每次扩容是创建新数组+复制。",
    "0.75": "HashMap负载因子0.75的原因：空间和时间的折中。太小(如0.5)：浪费空间(一半桶空着)但冲突少。太大(如0.99)：空间利用率高但冲突多(链表长→查找慢)。0.75是泊松分布计算的最优值：在随机哈希下,桶中元素数服从泊松分布,0.75时长度超过8的概率极低(约0.00000006),兼顾空间和性能。初始容量16=2^4,扩容为2倍(保证hash分布均匀)。",
    "关系型.*非关系型": "关系型数据库(MySQL/PostgreSQL)：表结构固定/SQL查询/ACID事务/JOIN关联/强一致性。非关系型NoSQL：①文档型(MongoDB,BSON,灵活Schema) ②键值型(Redis,高性能) ③列族(HBase,海量数据) ④图数据库(Neo4j,关系网络)。选型：需要强事务/复杂查询→MySQL 灵活Schema→MongoDB 高速缓存→Redis 全文检索→ES 海量写入→HBase。",
    "新生代.*算法": "新生代用复制算法(Copying)的原因：①新生代对象\"朝生夕死\"(98%对象很快死亡),存活对象少 ②复制算法只需复制存活对象(少量),效率高 ③Eden:Survivor=8:1:1,每次只浪费10%空间 ④Eden+From→To,存活对象集中到一个Survivor,另一个清空 ⑤老年代用标记-整理(Mark-Compact)因为存活对象多,复制代价大。G1不再严格分代,而是分Region。",
    "InnoDB.*页": "InnoDB存储引擎以页(Page)为单位管理数据,默认16KB。页结构：①File Header(页头,38字节,页号/前后指针) ②Page Header(页面状态信息) ③Infimum+Supremum(最小最大记录) ④User Records(用户记录) ⑤Free Space(空闲空间) ⑥Page Directory(页目录,二分查找定位记录) ⑦File Trailer(校验和,8字节)。一个16KB页能存~500行(按每行200字节估算)。B+树的每个节点就是一个页。",
    "Integer.*默认值": "Integer默认值null(是对象,不是基本类型)。int默认值0。区别：Integer可以为null(数据库NULL场景),int不能。自动拆箱时null会NPE(int i = nullInteger→NullPointerException)。Integer缓存：-128~127范围内Integer.valueOf()返回缓存对象(==比较为true),超出范围new对象(==为false)。面试常考：Integer a=127;Integer b=127; a==b→true; a=128;b=128; a==b→false。",
    "MCP.*协议": "Model Context Protocol,Anthropic提出的开放协议,标准化LLM与工具的连接。架构：MCP Host(Claude Desktop/AI IDE)→MCP Client(协议客户端)→MCP Server(工具/数据提供方)。传输：stdio(本地)/SSE(远程)。能力：Tools(函数调用)/Resources(数据读取)/Prompts(模板)。JSON-RPC协议。意义：一次实现Server,任何Host都能用(类似USB标准化外设)。",
    "分区表": "MySQL分区表：将一张大表按规则拆分为多个物理分区,逻辑上仍是一张表。类型：①Range(按范围,如按日期) ②List(按枚举值) ③Hash(按哈希) ④Key(按MySQL内部哈希)。好处：查询只需扫描相关分区(分区裁剪)/便于数据管理(删除旧分区极快)。注意：分区键必须在主键和唯一索引中。与分库分表区别：分区是MySQL内部实现,分库分表是应用层/中间件实现。",
    "must.*should": "Elasticsearch bool查询：①must(必须匹配,相当于AND,影响评分) ②should(可以匹配,相当于OR,影响评分) ③must_not(必须不匹配,相当于NOT,不影响评分) ④filter(必须匹配,不影响评分,可缓存)。规则：有must时should不强制,没有must时至少一个should必须匹配(minimum_should_match)。filter比must快(不计算评分+可缓存),精确过滤用filter,相关性搜索用must。",
    "多租户": "多租户(Multi-Tenancy)：一套系统服务多个租户(企业/组织)。隔离方案：①独立数据库(最强隔离,成本最高) ②共享数据库独立Schema(中等隔离) ③共享表+tenant_id字段(最常用,成本最低)。实现：①数据层：MyBatis拦截器自动加tenant_id条件 ②缓存层：Redis key加租户前缀 ③配置层：每租户独立配置。框架：Sa-Token多租户模式/自定义TenantFilter。",
    "端口.*修改": "SpringBoot修改端口：①application.yml中server.port=8090 ②启动参数--server.port=8090 ③环境变量SERVER_PORT=8090 ④编程式EmbeddedServletContainerCustomizer。优先级：命令行参数>环境变量>配置文件>默认值(8080)。",
    "稳定性": "系统稳定性建设：①监控(Prometheus+Grafana指标/SkyWalking链路/ELK日志) ②告警(核心指标异常→通知) ③限流(防止过载,Sentinel/Nginx) ④熔断(防止级联故障) ⑤降级(兜底方案) ⑥容灾(多活/异地备份) ⑦压测(定期压测发现瓶颈) ⑧混沌工程(Chaos Monkey随机故障注入) ⑨值班(7×24 oncall) ⑩复盘(故障后复盘总结)。",
    "前端.*参数.*后端": "前端参数传不到后端的排查：①检查请求方式(GET用@RequestParam/POST用@RequestBody) ②Content-Type是否匹配(form表单:application/x-www-form-urlencoded,JSON:application/json) ③参数名是否一致(用@RequestParam(\"name\")指定) ④@RequestBody需要JSON格式(前端用JSON.stringify) ⑤CORS跨域问题(@CrossOrigin或配置CorsFilter) ⑥SpringMVC参数绑定机制(@ModelAttribute自动绑定表单字段)。",
    "日期.*一年前": "Java获取一年前的日期：①LocalDate.now().minusYears(1)(Java 8+,推荐) ②Calendar.getInstance().add(Calendar.YEAR,-1)(旧API) ③new DateTime().minusYears(1)(Joda-Time)。格式化：DateTimeFormatter.ofPattern(\"yyyy-MM-dd\").format(date)。注意：时区问题(ZoneId.of(\"Asia/Shanghai\"))。Java 8+用java.time包(LocalDate/LocalDateTime/ZonedDateTime),不用Date/Calendar。",
    "查询.*列属性": "MySQL查看表的列信息：①DESC table_name(列名/类型/是否NULL/默认值) ②SHOW COLUMNS FROM table_name ③SELECT * FROM information_schema.COLUMNS WHERE TABLE_NAME='table_name'(最详细,包含注释/字符集等) ④SHOW CREATE TABLE table_name(完整建表语句)。Java中获取：DatabaseMetaData.getColumns()。",
    "用户在线": "在线用户统计：①Redis Bitmap(SETBIT online:2024-01-01 user_id 1,BITCOUNT统计) ②Redis SET(SADD online_users user_id,SCARD统计) ③Redis Sorted Set(ZADD with timestamp,ZRANGEBYSCORE过滤最近活跃) ④心跳(客户端定时上报,超时则下线) ⑤WebSocket长连接(连接数=在线数)。实时性要求高用心跳/长连接,统计用心跳+Redis。",
    "测试.*bug": "处理Bug流程：①复现(确认Bug存在和触发条件) ②分类(功能Bug/兼容性/性能/安全) ③定位(看日志/断点调试/二分法缩小范围) ④修复(修改代码+单元测试) ⑤自测(验证修复+回归测试) ⑥提交(代码Review+合并) ⑦通知测试(标注已修复) ⑧文档(记录Bug原因和修复方案)。态度：不否认不推诿,认真对待每个Bug。",
    "开发周期": "回答：简述项目周期和你的角色。如\"这个项目前后3个月,我参与了需求评审→技术方案设计→开发(2个月)→测试→上线的全流程,主要负责XX模块的后端开发\"。如果没有完整经历,说\"我负责的是迭代开发,每个迭代2周,包含需求评审→开发→Code Review→测试→发布\"。",
    "jdk版本": "常用JDK版本：①JDK8(LTS,最广泛,2014) ②JDK11(LTS,引入var/HttpClient,2018) ③JDK17(LTS,sealed classes/records,2021) ④JDK21(LTS,virtual threads/sequenced collections,2023)。面试回答：如实说用的版本,如果用过多个可以说\"项目中主要用JDK8/11,个人学习用过JDK17/21的新特性\"。注意：JDK8和JDK11是目前企业主流。",
    "ollama.*老数据": "Ollama本地大模型数据陈旧的解决：①RAG(检索增强生成)：将最新数据向量化→检索→注入context ②微调(在新数据上微调模型,成本高) ③Function Calling(让模型调用搜索引擎获取实时信息) ④定期更新模型(拉取最新版ollama模型) ⑤Prompt注入(在System Prompt中放最新关键信息)。推荐：RAG方案(最灵活,数据更新只需重新索引)。",
    "做过二次开发": "回答：有/没有+具体说明。如果有：\"基于XX开源项目做了二次开发,主要新增了XX功能/修改了XX模块,遇到了XX问题(如兼容性/升级维护),通过XX方式解决\"。如果没有：说\"虽然没有做过开源项目的二次开发,但我有阅读和理解开源源码的能力,如读过Spring/MyBatis的核心模块源码\"。",
    "数据量.*多少": "回答：如实说+优化措施。如\"订单表大约500万行,做了分库分表(按用户ID哈希分8个库)。日志表按天分表,每天约100万行,30天后归档到历史表\"。如果没上线：\"项目还在开发阶段,预计初期数据量在百万级,设计时已考虑分库分表方案\"。面试官关注：你对数据量的感知+是否做过性能优化。",
    "游戏服务端": "如实回答兴趣。如果感兴趣：\"我对游戏服务端开发很感兴趣,了解过游戏服务端的技术栈(如Netty网络框架/状态同步/帧同步/游戏AI),如果有合适的机会愿意尝试\"。如果不感兴趣：\"目前专注于Java后端开发,对游戏行业了解不多\"。诚实比迎合更重要。",
    "想到这边发展": "HR问题,如实回答。参考：\"这里有更多互联网公司和职业发展机会/我有朋友在这边/喜欢这个城市的生活节奏/之前的工作经验让我想在这个方向深耕\"。避免：说因为前公司不好。如果被追问\"能稳定吗\",给肯定回答。",
    "交换机.*类型": "RabbitMQ交换机：①Direct(routing key精确匹配) ②Fanout(广播所有绑定队列) ③Topic(通配符匹配：#匹配多个词,*匹配一个词) ④Headers(消息头匹配)。死信交换机(DLX)：消息被拒绝/超时/队列满→路由到DLX(用于延迟队列/重试)。默认交换机：routing key=队列名直连。",
    "最多.*数据": "回答框架：如实说+优化措施。如\"订单表最大约800万行,做了①分库分表(按user_id分8库16表) ②索引优化(user_id+status+create_time联合索引) ③归档(3个月前数据归到历史表) ④读写分离(写主库,读从库)\"。面试官看的是你对大数据量的处理经验。",
    "做过的功能": "回答框架：选一个有技术深度的功能。如\"文章发布审核功能：①技术方案(审核状态机+MQ异步审核) ②难点(审核超时处理+并发发布防重复) ③优化(Redis缓存热点文章,响应时间从2s降到200ms)\"。避免：说太简单的功能(如\"做了增删改查\")。",
    "olama.*大模型": "Ollama本地部署LLM。数据陈旧问题：模型训练数据有截止日期,无法获取最新信息。解决：①RAG(将最新文档向量化→检索→注入context) ②Function Calling(让模型调用搜索API获取实时信息) ③定期更新模型版本 ④Prompt注入关键最新信息。推荐RAG方案。",
    "jdk.*版本": "JDK版本选择：①JDK8(企业主流,稳定) ②JDK11(LTS,var语法/HttpClient) ③JDK17(LTS,sealed/records/增强switch) ④JDK21(LTS,virtual threads/pattern matching)。面试如实回答,如果用过多个版本更好。新项目推荐JDK17+,老项目JDK8+。注意：JDK9开始模块化(JPMS),升级可能有兼容性问题。",
    "交换机": "RabbitMQ Exchange(交换机)类型：①Direct(精确匹配routing key) ②Fanout(广播,忽略routing key) ③Topic(通配符匹配：*.log匹配a.log,#.log匹配a.b.log) ④Headers(消息头属性匹配)。绑定：Exchange→Queue通过Binding Key关联。死信Exchange(DLX)：处理失败/过期/满的消息。延迟队列：TTL+DLX实现。",
    "条件渲染": "Vue条件渲染：v-if(条件不满足则DOM不存在,切换开销大)/v-show(始终在DOM,display切换,初始渲染开销大)。v-if可配合v-else-if/v-else。React条件渲染：三元表达式(condition?<A/>:<B/>)/&&短路(condition&&<A/>)/提前return。框架原理：Virtual DOM Diff算法比较新旧VDOM→最小化真实DOM操作。",
    "it技术": "IT技术面试常见考点：①Java基础(集合/并发/JVM) ②框架(Spring/Boot/Cloud/MyBatis) ③数据库(MySQL索引/事务/优化) ④缓存(Redis数据类型/缓存问题) ⑤消息队列(Kafka/RabbitMQ) ⑥微服务(注册中心/网关/远程调用) ⑦分布式(锁/事务/ID) ⑧DevOps(Docker/Linux/Git) ⑨算法(排序/查找/DP) ⑩项目经验(STAR法则描述)。",
}

# Apply
patterns = []
for kw, answer in final_answers.items():
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
