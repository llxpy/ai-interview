import json, re

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Input: {len(data)} questions")

# === STEP 1: Better question cleaning ===
for q in data:
    text = q['question'].strip()
    
    # Remove "全是java se问题 2." style prefixes - extract the actual question
    m = re.match(r'^全是.*?问题\s*\d*[\.\)、]\s*', text)
    if m:
        text = text[m.end():].strip()
    
    # Remove trailing commentary
    text = re.sub(r'[,，\s]*尴尬了.*$', '', text)
    text = re.sub(r'[,，\s]*我感觉.*寄.*$', '', text)
    text = re.sub(r'[,，\s]*快寄了.*$', '', text)
    text = re.sub(r'[,，\s]*0\.0.*$', '', text)
    text = re.sub(r'\s*[-—]+\s*$', '', text)
    text = re.sub(r'？？+', '？', text)
    text = re.sub(r'^\d+[\.\)、]\s*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Add question mark if missing
    if text and not text.endswith(('？', '?', '。', '！', '嘛', '呢', '吧', '：', ':')):
        if any(kw in text for kw in ['什么', '怎么', '如何', '哪些', '为什么', '哪个', '是否', '有没有', '是不是', '区别', '原理', '实现', '理解', '介绍', '讲一下', '说一下', '描述']):
            text += '？'
    
    q['question'] = text

# === STEP 2: Remove non-technical / HR-only questions ===
hr_only = [
    r'^期望薪资', r'^期望的薪资', r'^目前.*薪资', r'^原来的薪资',
    r'^多久能到岗', r'^到岗时间', r'^目前在什么地方',
    r'^为什么离职', r'^离职原因', r'^之前离职',
    r'^你有什么优势$', r'^你对我们公司了解吗', r'^说一下你的职业规划',
    r'^职业规划$', r'^公司规模$', r'^项目组人数$', r'^项目.*几个人$',
    r'^你目前在', r'^能不能接收加班', r'^能不能接受加班',
    r'^疫苗几针', r'^在职还是离职', r'^为什么之前在老家',
    r'^之前在哪里工作$', r'^学习能力怎么样',
    r'^项目技术大概是多久可以上手',
    r'^负责过什么模块.*什么时候.*独立',
    r'^有什么要问我的', r'^还有什么要问',
    r'^感觉不像是', r'^面试全部问', r'^问的全是',
    r'^HR沟通薪资', r'^项目经理面.*问了问',
    r'^公司规模', r'^前两年.*收获', r'^对自己的.*规划',
    r'^平时会学习', r'^看.*相关书籍', r'^有没有看过.*官网',
    r'^有没有和客户聊过需求',
    r'^平常的工作流程$', r'^有自己编写过文档吗$',
    r'^计划用户量', r'^企业结构及分工', r'^平时怎样学习新知识',
    r'^自我介绍$', r'^项目介绍$', r'^介绍项目$', r'^聊聊项目$',
    r'^项目.*做了啥$', r'^讲一下.*最近.*项目$', r'^讲一下你负责的模块$',
    r'^之前做过什么项目$', r'^讲一下.*项目框架$',
    r'^聊项目$', r'^项目中.*职能涉及', r'^聊聊项目$',
]

hr_pats = [re.compile(p, re.IGNORECASE) for p in hr_only]

filtered = []
for q in data:
    text = q['question'].strip()
    if len(text) < 5:
        continue
    skip = False
    for pat in hr_pats:
        if pat.search(text):
            skip = True
            break
    if skip:
        continue
    filtered.append(q)

print(f"After HR filter: {len(filtered)} questions")

# === STEP 3: Re-assign IDs ===
for i, q in enumerate(filtered):
    q['id'] = i + 1

# === STEP 4: Save ===
with open('public/data.json', 'w', encoding='utf-8') as f:
    json.dump(filtered, f, ensure_ascii=False)

print(f"Final: {len(filtered)} questions saved")

# Stats
from collections import Counter
cats = Counter(q['category'] for q in filtered)
for c, n in cats.most_common():
    print(f"  {c}: {n}")
