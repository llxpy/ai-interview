import json, re

with open('public/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Categorize answer quality
good = 0       # Has real detailed answer (>50 chars, not template)
medium = 0     # Has some content but generic
bad = 0        # Empty or "暂无" template
bad_samples = []

for q in data:
    a = q['answer']
    if not a or len(a) < 20:
        bad += 1
        bad_samples.append(q['question'][:50])
    elif '暂无标准答案' in a or '这是一道' in a or '通用参考' in a or '结合自己项目' in a:
        bad += 1
        bad_samples.append(q['question'][:50])
    elif len(a) > 100:
        good += 1
    else:
        medium += 1

print(f"Total: {len(data)}")
print(f"Good (>100 chars, real answer): {good} ({good*100//len(data)}%)")
print(f"Medium (20-100 chars): {medium} ({medium*100//len(data)}%)")
print(f"Bad (empty/template): {bad} ({bad*100//len(data)}%)")
print(f"\nBad samples ({min(20, len(bad_samples))}):")
for s in bad_samples[:20]:
    print(f"  - {s}")

# Per category
from collections import defaultdict
cat_stats = defaultdict(lambda: {'good': 0, 'medium': 0, 'bad': 0, 'total': 0})
for q in data:
    a = q['answer']
    cat = q['category']
    cat_stats[cat]['total'] += 1
    if not a or len(a) < 20 or '暂无标准答案' in a or '这是一道' in a or '通用参考' in a or '结合自己项目' in a:
        cat_stats[cat]['bad'] += 1
    elif len(a) > 100:
        cat_stats[cat]['good'] += 1
    else:
        cat_stats[cat]['medium'] += 1

print(f"\n{'Category':<15} {'Good':>6} {'Med':>6} {'Bad':>6} {'Total':>6} {'Bad%':>6}")
for cat, s in sorted(cat_stats.items(), key=lambda x: -x[1]['bad']):
    pct = s['bad']*100//s['total'] if s['total'] else 0
    print(f"{cat:<15} {s['good']:>6} {s['medium']:>6} {s['bad']:>6} {s['total']:>6} {pct:>5}%")
